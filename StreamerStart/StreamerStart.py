import AlteryxPythonSDK as Sdk
import asyncio


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "StreamerStart (" + str(n_tool_id) + ")"

        # Custom properties
        self.loop = asyncio.get_event_loop()
        self.Output: Sdk.OutputAnchor = None
        self.Info: Sdk.RecordInfo = None
        self.Creator: Sdk.RecordCreator = None
        self.Loop = None

    def pi_init(self, str_xml: str):
        # Getting the output anchor from Config.xml by the output connection name
        self.Output = self.output_anchor_mgr.get_output_anchor('Output')

    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        return None

    def pi_add_outgoing_connection(self, str_name: str) -> bool:
        return True

    def pi_push_all_records(self, n_record_limit: int) -> bool:
        self.Info = self._generate_output_record_info()
        self.Output.init(self.Info)
        self.Creator = self.Info.construct_record_creator()

        update_only = self.alteryx_engine.get_init_var(self.n_tool_id, 'UpdateOnly') == 'True'
        if update_only:
            return True

        self.display_info_msg("Streamer start is starting")
        self._push_record("Start")
        self.Loop = self.loop.create_task(self._wait_for_close())
        self.loop.run_until_complete(self.Loop)
        return True

    def pi_close(self, b_has_errors: bool):
        self.display_info_msg("Streamer start is closing...")
        if self.Loop is not None:
            self.Loop.cancel()
            self._push_record("End")
            self.Output.close()
            self.display_info_msg("Streamer start has closed")

    def display_error_msg(self, msg_string: str):
        self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.error, msg_string)

    def display_info_msg(self, msg_string: str):
        self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.info, msg_string)

    def _generate_output_record_info(self) -> Sdk.RecordInfo:
        info: Sdk.RecordInfo = Sdk.RecordInfo(self.alteryx_engine)
        info.add_field("Event", Sdk.FieldType.v_wstring, 1073741823, 0, self.label)
        return info

    def _push_record(self, event: str):
        self.Creator.reset()
        self.Info[0].set_from_string(self.Creator, event)
        data = self.Creator.finalize_record()
        self.Output.push_record(data)

    @staticmethod
    async def _wait_for_close():
        await asyncio.sleep(30)
        return
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            return
