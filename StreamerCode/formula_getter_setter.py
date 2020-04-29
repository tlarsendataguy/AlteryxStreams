from datetime import datetime
from typing import Callable
import AlteryxPythonSDK as Sdk


integer_types = [Sdk.FieldType.byte, Sdk.FieldType.int16, Sdk.FieldType.int32, Sdk.FieldType.int64]
decimal_types = [Sdk.FieldType.fixeddecimal, Sdk.FieldType.float, Sdk.FieldType.double]
string_types = [Sdk.FieldType.string, Sdk.FieldType.wstring, Sdk.FieldType.v_string, Sdk.FieldType.v_wstring]


def set_field(field: Sdk.Field, creator: Sdk.RecordCreator, value) -> bool:
    if field.type in string_types:
        field.set_from_string(creator, str(value))
    elif field.type in integer_types:
        field.set_from_int64(creator, int(value))
    elif field.type in decimal_types:
        field.set_from_double(creator, float(value))
    elif field.type == Sdk.FieldType.date:
        field.set_from_string(creator, datetime.strftime(value, "%Y-%m-%d"))
    elif field.type == Sdk.FieldType.datetime:
        field.set_from_string(creator, datetime.strftime(value, "%Y-%m-%d %H:%M:%S"))
    else:
        return False
    return True


# self must have the following properties:
#   Record: Sdk.RecordRef


def generate_getter(self, field: Sdk.Field) -> Callable:
    def getter():
        if field.type in integer_types:
            return field.get_as_int64(self.Record)
        if field.type in decimal_types:
            return field.get_as_double(self.Record)
        if field.type in string_types:
            return field.get_as_string(self.Record)
        if field.type == Sdk.FieldType.date:
            return datetime.strptime(field.get_as_string(self.Record), "%Y-%m-%d")
        if field.type == Sdk.FieldType.datetime:
            return datetime.strptime(field.get_as_string(self.Record), "%Y-%m-%d %H:%M:%S")
        return None

    return getter
