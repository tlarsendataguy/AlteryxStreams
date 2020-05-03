import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Event Hubs In (" + str(n_tool_id) + ")"

        # Custom properties
        self.Output: Sdk.OutputAnchor = None
        self.CheckpointConnStr = ''
        self.CheckpointContainer = ''
        self.EventHubsConnStr = ''
        self.ConsumerGroup = ''
        self.EventHubName = ''

    def pi_init(self, str_xml: str):
        xml = Et.fromstring(str_xml)
        self.CheckpointConnStr = xml.find("CheckpointConnStr").text if 'CheckpointConnStr' in str_xml else ''
        self.CheckpointContainer = xml.find("CheckpointContainer").text if 'CheckpointContainer' in str_xml else ''
        self.EventHubsConnStr = xml.find("EventHubsConnStr").text if 'EventHubsConnStr' in str_xml else ''
        self.ConsumerGroup = xml.find("ConsumerGroup").text if 'ConsumerGroup' in str_xml else ''
        self.EventHubName = xml.find("EventHubName").text if 'EventHubName' in str_xml else ''
        if self.CheckpointConnStr == '' or self.CheckpointContainer == '' or self.EventHubsConnStr == ''\
                or self.ConsumerGroup == '' or self.EventHubName == '':
            self.display_error_msg('One or more parameters were empty.  All configuration parameters are required.')

        # Getting the output anchor from Config.xml by the output connection name
        self.Output = self.output_anchor_mgr.get_output_anchor('Output')

    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        return IncomingInterface(self)

    def pi_add_outgoing_connection(self, str_name: str) -> bool:
        return True

    def pi_push_all_records(self, n_record_limit: int) -> bool:
        return False

    def pi_close(self, b_has_errors: bool):
        return

    def display_error_msg(self, msg_string: str):
        self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.error, msg_string)

    def display_info_msg(self, msg_string: str):
        self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.info, msg_string)


class IncomingInterface:
    def __init__(self, parent: AyxPlugin):
        # Default properties
        self.parent: AyxPlugin = parent
        self.RecordInfo = Sdk.RecordInfo(self.parent.alteryx_engine)
        self.MessageField = self.RecordInfo.add_field("Message", Sdk.FieldType.v_wstring, 1073741823, 0, self.parent.label)
        self.Creator = self.RecordInfo.construct_record_creator()

        # Custom properties
        self.EventField: Sdk.Field = None
        self.Client = None

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.EventField = record_info_in.get_field_by_name('Event')
        if self.EventField is None:
            self.parent.display_error_msg("Incoming data source must contain an 'Event' text field that pushes 'Start' and 'End' events")
            return False
        self.parent.Output.init(self.RecordInfo)
        checkpoint_store = BlobCheckpointStore.from_connection_string(self.parent.CheckpointConnStr,
                                                                      self.parent.CheckpointContainer)
        self.Client = EventHubConsumerClient.from_connection_string(self.parent.EventHubsConnStr,
                                                                    consumer_group=self.parent.ConsumerGroup,
                                                                    eventhub_name=self.parent.EventHubName,
                                                                    checkpoint_store=checkpoint_store)
        self.parent.display_info_msg("Event Hubs receive client created")
        return True

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        self.parent.display_info_msg("received an event")
        event = self.EventField.get_as_string(in_record)
        if event != 'Start':
            asyncio.wait_for(asyncio.ensure_future(self.Client.close()), timeout=-1)
            self.parent.display_info_msg('stopped event loop')
            return True
        asyncio.ensure_future(self._async_push())
        self.parent.display_info_msg("started event loop")
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        self.parent.Output.assert_close()
        return

    async def _async_push(self):
        try:
            await self.Client.receive(on_event=self._push_event, on_error=self._receive_error)
        except asyncio.CancelledError:
            self.parent.display_info_msg("was cancelled")
            return
        except Exception as ex:
            self.parent.display_error_msg("Error in _async_push: " + str(ex))

    async def _push_event(self, partition_context, event):
        checkpoint_future = partition_context.update_checkpoint(event)
        self.Creator.reset()
        self.MessageField.set_from_string(self.Creator, event.body_as_str(encoding='UTF-8'))
        output = self.Creator.finalize_record()
        self.parent.Output.push_record(output)
        await checkpoint_future

    async def _receive_error(self, partition_context, exception):
        self.parent.display_error_msg("Received error from Event Hubs: " + str(exception))
