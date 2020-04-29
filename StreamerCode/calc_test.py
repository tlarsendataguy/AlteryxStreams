from typing import Callable
from formula_visitor import FormulaVisitor
import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Calc Test (" + str(n_tool_id) + ")"

        # Custom properties
        self.Output: Sdk.OutputAnchor = None
        self.Formula: str = ''

    def pi_init(self, str_xml: str):
        self.Formula = Et.fromstring(str_xml).find("Formula").text if 'Formula' in str_xml else ''
        if self.Formula == '':
            self.display_error_msg('No formula was provided')

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
        self.IncomingInfo: Sdk.RecordInfo = None
        self.Copier: Sdk.RecordCopier = None
        self.Creator: Sdk.RecordCreator = None
        self.Record: Sdk.RecordRef = None
        self.Fields: map[str, Callable] = {}
        self.Visitor: FormulaVisitor = None

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.IncomingInfo = record_info_in
        self.Info = self.IncomingInfo.clone()
        self.Info.add_field("Calc", Sdk.FieldType.int64, 8, 0)
        self.Creator = self.Info.construct_record_creator()
        self.Copier = Sdk.RecordCopier(self.Info, self.IncomingInfo)
        index = 0
        while index < self.IncomingInfo.num_fields:
            self.Copier.add(index, index)
            field = record_info_in[index]
            self.Fields[field.name] = lambda: field.get_as_int64(self.Record)
            index += 1
        self.Copier.done_adding()
        self.parent.Output.init(self.Info)
        try:
            self.Visitor = FormulaVisitor(expression=self.parent.Formula, fields=self.Fields)
            return True
        except Exception as ex:
            self.parent.display_error_msg(str(ex))
            return False

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        self.Record = in_record
        self.Creator.reset()
        self.Copier.copy(self.Creator, in_record)
        try:
            result = self.Visitor.calculate()
            self.Info.get_field_by_name('Calc').set_from_int64(self.Creator, result)
            data = self.Creator.finalize_record()
            self.parent.Output.push_record(data)
            return True
        except Exception as ex:
            self.parent.display_error_msg(str(ex))
            return False

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        self.parent.Output.assert_close()
        return
