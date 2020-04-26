import AlteryxPythonSDK as Sdk


class AyxPlugin:
    def display_error_msg(self, msg_string: str):
        return

    def display_info_msg(self, msg_string: str):
        return

    def update_progress(self, percent):
        return

    def ii_init(self, record_info: Sdk.RecordInfo, connection: str):
        return

    def ii_push_record(self, record: Sdk.RecordCreator, connection: str):
        return


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
        self.parent.ii_push_record(creator, self.connection)
        return True

    def ii_update_progress(self, d_percent: float):
        # Inform the Alteryx engine of the tool's progress.
        self.parent.update_progress(d_percent)

    def ii_close(self):
        return
