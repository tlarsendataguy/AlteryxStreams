import asyncio
import json
from typing import Dict
from formula_getter_setter import integer_types, decimal_types
import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
from azure.eventhub import EventHubProducerClient, EventData

class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Event Hubs Out (" + str(n_tool_id) + ")"

        # Custom properties
        self.EventHubsConnStr = ''
        self.EventHubName = ''

    def pi_init(self, str_xml: str):
        xml = Et.fromstring(str_xml)
        self.EventHubsConnStr = xml.find("EventHubsConnStr").text if 'EventHubsConnStr' in str_xml else ''
        self.EventHubName = xml.find("EventHubName").text if 'EventHubName' in str_xml else ''
        if self.EventHubsConnStr == '' or self.EventHubName == '':
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
        self.Producer: EventHubProducerClient = None
        self.DataMap: Dict[str, any] = {}

    def ii_init(self, record_info_in: Sdk.RecordInfo) -> bool:
        self.Info = record_info_in
        self.Producer = EventHubProducerClient.from_connection_string(conn_str=self.parent.EventHubsConnStr,
                                                                      eventhub_name=self.parent.EventHubName)
        for field in self.Info:
            self.DataMap[field.name] = None
        self.parent.display_info_msg("Event Hubs producer client created")
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
        event_data = EventData(encoded)
        batch = self.Producer.create_batch()
        batch.add(event_data)
        try:
            self.Producer.send_batch(batch)
        except Exception as ex:
            self.parent.display_error_msg('Error sending to Azure Event Hubs: ' + str(ex))
        self.parent.display_info_msg('sent message')
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

    def ii_close(self):
        return
