import AlteryxPythonSDK as Sdk
import incoming_interface as ii


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Sample (" + str(n_tool_id) + ")"

        # Custom properties
        self.Output: Sdk.OutputAnchor = None
        self.RecordInfo: Sdk.RecordInfo = None
        self.Creator: Sdk.RecordCreator = None

    def pi_init(self, str_xml: str):
        # Getting the output anchor from Config.xml by the output connection name
        self.Output = self.output_anchor_mgr.get_output_anchor('Output')

    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        return ii.IncomingInterface(self, str_type)

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

    def update_progress(self, percent):
        self.alteryx_engine.output_tool_progress(self.n_tool_id, percent)

    def ii_init(self, record_info: Sdk.RecordInfo, connection: str):
        if connection == 'Left':
            self.RecordInfo = record_info
            self.Output.init(self.RecordInfo)

    def ii_push_record(self, record: Sdk.RecordCreator, connection: str):
        if connection == 'Left':
            self.Creator = record
            return

        if self.Creator is None:
            return

        output = self.Creator.finalize_record()
        self.Output.push_record(output)
