import random
import threading

import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
import asyncio


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Streamer (" + str(n_tool_id) + ")"

        # Custom properties
        self.Output: Sdk.OutputAnchor = None

    def pi_init(self, str_xml: str):
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

        # Custom properties
        self.RecordInfo: Sdk.RecordInfo = None
        self.Creator: Sdk.RecordCreator = None
        self.EventField: Sdk.Field = None
        self.LoopTask = None

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.EventField = record_info_in.get_field_by_name('Event')
        if self.EventField is None:
            self.parent.display_error_msg("Incoming data source must contain an 'Event' text field that pushes 'Start' and 'End' events")
            return False
        self.RecordInfo = self._generate_output_record_info()
        self.Creator = self.RecordInfo.construct_record_creator()
        self.parent.Output.init(self.RecordInfo)
        return True

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        self.parent.display_info_msg("received an event")
        event = self.EventField.get_as_string(in_record)
        if event != 'Start':
            if self.LoopTask is not None:
                self.LoopTask.cancel()
                self.parent.display_info_msg("stopped event loop")
            return True
        event_loop = asyncio.get_event_loop()
        self.LoopTask = event_loop.create_task(self._asyncPush())
        threading.Thread(target=self.LoopTask).start()
        self.parent.display_info_msg("started event loop")
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        self.parent.Output.assert_close()
        return

    def _generate_output_record_info(self) -> Sdk.RecordInfo:
        info: Sdk.RecordInfo = Sdk.RecordInfo(self.parent.alteryx_engine)
        info.add_field("Source", Sdk.FieldType.v_wstring, 1073741823, 0, self.parent.label)
        info.add_field("Count", Sdk.FieldType.int64, 0, 0, self.parent.label)
        return info

    async def _asyncPush(self):
        count: int = 0
        wait: int = random.randint(1, 5)
        self.parent.display_info_msg("will wait for " + str(wait) + " seconds")

        try:
            while True:
                await asyncio.sleep(wait)
                count += 1
                self.Creator.reset()
                self.RecordInfo.get_field_by_name('Source').set_from_string(self.Creator, self.parent.label)
                self.RecordInfo.get_field_by_name('Count').set_from_int64(self.Creator, count)
                data = self.Creator.finalize_record()
                self.parent.Output.push_record(data)
        except asyncio.CancelledError:
            self.parent.display_info_msg("was cancelled")
            return
