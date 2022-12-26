import shutil
from .input_item import InputItem


class InputItemLocal(InputItem):
    def __init__(self, *, resource_id, language_code, path):
        super().__init__(resource_id=resource_id, language_code=language_code)
        self.origin_filepath = path

    def download(self, destination_filepath):
        shutil.copyfile(self.origin_filepath, destination_filepath)
