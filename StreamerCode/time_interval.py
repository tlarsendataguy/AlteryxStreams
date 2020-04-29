import datetime

import AlteryxPythonSDK as Sdk


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Time Interval (" + str(n_tool_id) + ")"

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
        self.Info: Sdk.RecordInfo = None
        self.Creator: Sdk.RecordCreator = None
        self.LastTime: datetime.datetime = None

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.Info = Sdk.RecordInfo(self.parent.alteryx_engine)
        self.Info.add_field('Time Interval', Sdk.FieldType.int64, 8, 0)
        self.Creator = self.Info.construct_record_creator()
        self.parent.Output.init(self.Info)
        self.LastTime = datetime.datetime.now()
        return True

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        now = datetime.datetime.now()
        delta = int((now - self.LastTime) / datetime.timedelta(milliseconds=1))
        self.Creator.reset()
        self.Info[0].set_from_int64(self.Creator, delta)
        output = self.Creator.finalize_record()
        self.parent.Output.push_record(output)
        self.LastTime = now
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        self.parent.Output.assert_close()
        return
