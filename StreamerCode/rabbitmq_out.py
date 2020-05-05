import json
from typing import Dict
from formula_getter_setter import integer_types, decimal_types
import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
import pika


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "RabbitMQ Out (" + str(n_tool_id) + ")"

        # Custom properties
        self.Host = ''
        self.Queue = ''

    def pi_init(self, str_xml: str):
        xml = Et.fromstring(str_xml)
        self.Host = xml.find("Host").text if 'Host' in str_xml else ''
        self.Queue = xml.find("Queue").text if 'Queue' in str_xml else ''
        if self.Host == '' or self.Queue == '':
            self.display_error_msg('One or more parameters were empty.  All configuration parameters are required.')

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
        self.Info: Sdk.RecordInfo = None
        self.Connection: pika.BlockingConnection = None
        self.Channel = None
        self.DataMap: Dict[str, any] = {}

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.Info = record_info_in
        self.Connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.parent.Host))
        self.Channel = self.Connection.channel()
        self.Channel.queue_declare(self.parent.Queue)
        for field in self.Info:
            self.DataMap[field.name] = None
        self.parent.display_info_msg("RabbitMQ connection created")
        return True

    def ii_push_record(self, in_record: Sdk.RecordRef) -> bool:
        for field in self.Info:
            if field.get_null(in_record):
                self.DataMap[field.name] = None
            elif field.type in integer_types:
                self.DataMap[field.name] = field.get_as_int64(in_record)
            elif field.type in decimal_types:
                self.DataMap[field.name] = field.get_as_double(in_record)
            else:
                self.DataMap[field.name] = field.get_as_string(in_record)

        encoded = json.dumps(self.DataMap)

        try:
            self.Channel.basic_publish(exchange='', routing_key=self.parent.Queue, body=encoded)
        except Exception as ex:
            self.parent.display_error_msg('Error sending to RabbitMQ: ' + str(ex))
        self.parent.display_info_msg('sent message')
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        return
