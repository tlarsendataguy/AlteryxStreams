import collections
import AlteryxPythonSDK as Sdk


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Streamer Zip (" + str(n_tool_id) + ")"

        # Custom properties
        self.Output: Sdk.OutputAnchor = None
        self.LeftRecordInfo: Sdk.RecordInfo = None
        self.RightRecordInfo: Sdk.RecordInfo = None
        self.RecordInfo: Sdk.RecordInfo = None
        self.Creator: Sdk.RecordCreator = None
        self.LeftCopier: Sdk.RecordCopier = None
        self.RightCopier: Sdk.RecordCopier = None
        self.LeftRecords = collections.deque()
        self.RightRecords = collections.deque()

    def pi_init(self, str_xml: str):
        # Getting the output anchor from Config.xml by the output connection name
        self.Output = self.output_anchor_mgr.get_output_anchor('Output')

    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        return IncomingInterface(self, str_type)

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

    def ii_init(self, record_info: Sdk.RecordInfo, connection: str):
        if connection == 'Left':
            self.LeftRecordInfo = record_info
        else:
            self.RightRecordInfo = record_info
        if self._can_init_info():
            self._init_info()
        return

    def ii_push_record(self, record: Sdk.RecordRef, connection: str):
        if connection == 'Left':
            self.LeftRecords.append(record)
        else:
            self.RightRecords.append(record)

        if len(self.LeftRecords) == 0 or len(self.RightRecords) == 0:
            return

        left_record = self.LeftRecords.popleft()
        right_record = self.RightRecords.popleft()
        self.Creator.reset()
        self.LeftCopier.copy(self.Creator, left_record)
        self.RightCopier.copy(self.Creator, right_record)
        output = self.Creator.finalize_record()
        self.Output.push_record(output)

    def _can_init_info(self) -> bool:
        return self.LeftRecordInfo is not None and self.RightRecordInfo is not None

    def _init_info(self):
        self.RecordInfo = Sdk.RecordInfo(self.alteryx_engine)
        for field in self.LeftRecordInfo:
            self.RecordInfo.add_field(field)
        for field in self.RightRecordInfo:
            self.RecordInfo.add_field(field)
        self.Output.init(self.RecordInfo)
        self.Creator = self.RecordInfo.construct_record_creator()
        self.LeftCopier = Sdk.RecordCopier(self.RecordInfo, self.LeftRecordInfo)
        source_index = 0
        dest_index = 0
        for _ in self.LeftRecordInfo:
            self.LeftCopier.add(dest_index, source_index)
            source_index += 1
            dest_index += 1
        self.LeftCopier.done_adding()

        self.RightCopier = Sdk.RecordCopier(self.RecordInfo, self.RightRecordInfo)
        source_index = 0
        for _ in self.RightRecordInfo:
            self.RightCopier.add(dest_index, source_index)
            source_index += 1
            dest_index += 1
        self.RightCopier.done_adding()


class IncomingInterface:
    def __init__(self, parent: AyxPlugin, connection: str):
        # Default properties
        self.parent: AyxPlugin = parent
        self.connection: str = connection
        self.copier: Sdk.RecordCopier = None
        self.info: Sdk.RecordInfo = None

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.copier = Sdk.RecordCopier(record_info_in, record_info_in)
        for index in range(record_info_in.num_fields):
            self.copier.add(index, index)
        self.copier.done_adding()
        self.info = record_info_in
        self.parent.ii_init(record_info_in, self.connection)
        return True

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        # If we do not copy in_record here, this tool does not work.  The in_record reference becomes
        # invalid after this method returns

        creator = self.info.construct_record_creator()
        self.copier.copy(creator, in_record)
        copy = creator.finalize_record()
        self.parent.ii_push_record(copy, self.connection)
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        return
