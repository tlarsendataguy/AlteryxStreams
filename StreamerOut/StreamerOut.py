import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Streamer Output (" + str(n_tool_id) + ")"

        # Custom properties
        self.FilePath: str = ""

    def pi_init(self, str_xml: str):
        self.FilePath = Et.fromstring(str_xml).find('File').text if 'File' in str_xml else None

    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        return IncomingInterface(self)

    def pi_add_outgoing_connection(self, str_name: str) -> bool:
        return False

    def pi_push_all_records(self, n_record_limit: int) -> bool:
        self.display_error_msg('No input connection provided')
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

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.RecordInfo = record_info_in
        return True

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        with open(self.parent.FilePath, 'a') as file:
            field: int = 0
            while field < self.RecordInfo.num_fields-1:
                file.write(self.RecordInfo[field].get_as_string(in_record))
                file.write(',')
                field += 1
            file.write(self.RecordInfo[field].get_as_string(in_record))
            file.write('\n')
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        return
