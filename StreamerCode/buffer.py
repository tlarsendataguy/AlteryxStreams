from typing import List
import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Buffer (" + str(n_tool_id) + ")"

        # Custom properties
        self.Output: Sdk.OutputAnchor = None
        self.Records: int = 0

    def pi_init(self, str_xml: str):
        self.Records = int(Et.fromstring(str_xml).find("Records").text) if 'Records' in str_xml else 0
        if self.Records <= 0:
            self.display_error_msg('Seconds between records must be a positive, non-zero number')

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
        self.IncomingInfo: Sdk.RecordInfo = None
        self.Info: Sdk.RecordInfo = None
        self.Creator: Sdk.RecordCreator = None
        self.EventField: Sdk.Field = None
        self.LoopTask = None
        self.Index = 0
        self.Copiers: List[Sdk.RecordCreator] = []

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.IncomingInfo = record_info_in
        self.Info = Sdk.RecordInfo(self.parent.alteryx_engine)
        dest_index = 0
        for i in range(0, self.parent.Records):
            source_index = 0
            copier = Sdk.RecordCopier(self.Info, self.IncomingInfo)
            for field in self.IncomingInfo:
                self.Info.add_field('{name} {index}'.format(name=field.name, index=i+1),
                                    field.type,
                                    field.size,
                                    field.scale,
                                    field.source,
                                    field.description)
                copier.add(dest_index, source_index)
                dest_index += 1
                source_index += 1
            copier.done_adding()
            self.Copiers.append(copier)
        self.Creator = self.Info.construct_record_creator()
        self.parent.Output.init(self.Info)
        return True

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        self.Copiers[self.Index].copy(self.Creator, in_record)
        self.Index += 1
        if self.Index == self.parent.Records:
            output = self.Creator.finalize_record()
            self.parent.Output.push_record(output)
            self.Creator.reset()
            for field in self.Info:
                field.set_null(self.Creator)
            self.Index = 0
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        final_output = self.Creator.finalize_record()
        self.parent.Output.push_record(final_output)
        self.parent.Output.assert_close()
        return
