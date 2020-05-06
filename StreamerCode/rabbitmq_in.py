import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
import asyncio
import pika


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "RabbitMQ In (" + str(n_tool_id) + ")"

        # Custom properties
        self.Output: Sdk.OutputAnchor = None
        self.Host = ''
        self.Queue = ''

    def pi_init(self, str_xml: str):
        xml = Et.fromstring(str_xml)
        self.Host = xml.find("Host").text if 'Host' in str_xml else ''
        self.Queue = xml.find("Queue").text if 'Queue' in str_xml else ''
        if self.Host == '' or self.Queue == '':
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
        self.Connection: pika.SelectConnection = None
        self.Channel = None
        self.Loop = None

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.EventField = record_info_in.get_field_by_name('Event', throw_error=False)
        if self.EventField is None:
            self.parent.display_error_msg("Incoming data source must contain an 'Event' text field that pushes 'Start' and 'End' events")
            return False
        self.parent.Output.init(self.RecordInfo)
        self.Loop = asyncio.get_event_loop()
        self.Connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.parent.Host))
        self.Channel = self.Connection.channel()
        self.Channel.queue_declare(self.parent.Queue)
        self.Channel.basic_consume(queue=self.parent.Queue, on_message_callback=self._push_event, auto_ack=True)
        self.parent.display_info_msg("RabbitMQ connection created")
        return True

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        self.parent.display_info_msg("received an event")
        event = self.EventField.get_as_string(in_record)
        if event != 'Start':
            self.Connection.close()
            self.parent.display_info_msg('stopped event loop')
            return True
        self.Loop.run_in_executor(None, self.Channel.start_consuming)
        self.parent.display_info_msg("started event loop")
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        self.parent.Output.assert_close()
        return

    def _push_event(self, ch, method, properties, body):
        self.Creator.reset()
        self.MessageField.set_from_string(self.Creator, body.decode("utf-8"))
        output = self.Creator.finalize_record()
        self.parent.Output.push_record(output)
