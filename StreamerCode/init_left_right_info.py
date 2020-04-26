import AlteryxPythonSDK as Sdk


# self must have the following properties:
#   Output: Sdk.OutputAnchor
#   LeftRecordInfo: Sdk.RecordInfo
#   RightRecordInfo: Sdk.RecordInfo


def can(self) -> bool:
    return self.LeftRecordInfo is not None and self.RightRecordInfo is not None


def info(self):
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
