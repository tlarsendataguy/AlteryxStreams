from typing import Callable, Dict
from formula_visitor import FormulaVisitor, calculate
import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
from formula_getter_setter import generate_getter, set_field


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Reduce (" + str(n_tool_id) + ")"

        # Custom properties
        self.Output: Sdk.OutputAnchor = None
        self.Formula: str = ''
        self.FieldName: str = ''
        self.DataType: str = ''
        self.InitialValue: str = ''

    def pi_init(self, str_xml: str):
        self.Formula = Et.fromstring(str_xml).find("Formula").text if 'Formula' in str_xml else ''
        self.FieldName = Et.fromstring(str_xml).find("FieldName").text if 'FieldName' in str_xml else ''
        self.DataType = Et.fromstring(str_xml).find("DataType").text if 'DataType' in str_xml else ''
        self.InitialValue = Et.fromstring(str_xml).find("InitialValue").text if 'InitialValue' in str_xml else ''
        if self.Formula == '' or self.FieldName == '' or self.DataType == '' or self.InitialValue == '':
            self.display_error_msg('The field name, data type, formula, or initial value are blank.  All values must be provided.')

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
        self.Creator: Sdk.RecordCreator = None
        self.Record: Sdk.RecordRef = None
        self.Fields: Dict[str, Callable] = {}
        self.Visitor: FormulaVisitor = None
        self.CurrentValue = None
        self.CalcField: Sdk.Field = None

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.IncomingInfo = record_info_in
        index = 0
        while index < self.IncomingInfo.num_fields:
            field = self.IncomingInfo[index]
            self.Fields[field.name] = generate_getter(self, field)
            index += 1

        self.Info = Sdk.RecordInfo(self.parent.alteryx_engine)
        if self.parent.DataType == 'String':
            self.CalcField = self.Info.add_field(self.parent.FieldName, Sdk.FieldType.v_wstring, 1073741823, 0)
        elif self.parent.DataType == 'Integer':
            self.CalcField = self.Info.add_field(self.parent.FieldName, Sdk.FieldType.int64, 8, 0)
        elif self.parent.DataType == 'Decimal':
            self.CalcField = self.Info.add_field(self.parent.FieldName, Sdk.FieldType.double, 8, 0)
        elif self.parent.DataType == 'Date':
            self.CalcField = self.Info.add_field(self.parent.FieldName, Sdk.FieldType.date, 10, 0)
        elif self.parent.DataType == 'Datetime':
            self.CalcField = self.Info.add_field(self.parent.FieldName, Sdk.FieldType.datetime, 19, 0)
        else:
            self.parent.display_error_msg("Invalid data type: {datatype}".format(datatype=self.parent.DataType))
            return False

        self.Creator = self.Info.construct_record_creator()
        self.parent.Output.init(self.Info)
        try:
            self.CurrentValue = calculate(expression=self.parent.InitialValue, fields={})
            self.Fields[self.parent.FieldName] = lambda: self.CurrentValue
            self.Visitor = FormulaVisitor(expression=self.parent.Formula, fields=self.Fields)
            return True
        except Exception as ex:
            self.parent.display_error_msg(str(ex))
            return False

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        self.Record = in_record
        try:
            self.CurrentValue = self.Visitor.calculate()
            return True
        except Exception as ex:
            self.parent.display_error_msg(str(ex))
            return False

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        self.Creator.reset()
        success = set_field(self.CalcField, self.Creator, self.CurrentValue)
        if not success:
            self.parent.display_error_msg("Invalid data type: {datatype}".format(datatype=self.parent.DataType))
            return False

        data = self.Creator.finalize_record()
        self.parent.Output.push_record(data)
        self.parent.Output.assert_close()
        return
