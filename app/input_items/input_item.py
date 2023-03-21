from datetime import datetime
from pathlib import Path
import threading
import os
from abc import ABC, abstractmethod

class InputItem(ABC):
    def __init__(self, *, resource_id, recognizer_data):
        self.resource_id = int(resource_id) or -1
        self.recognizer_data = recognizer_data
        self.recognition_id = f"{threading.get_ident()}-{self.resource_id}-{datetime.utcnow().strftime('%m-%d.%H:%M:%S%f')}"
        self.extension = None

    def __str__(self):
        attributes_str = ''
        for item in self.__dict__:
            item_str = '{} = {}'.format(item, self.__dict__[item])
            attributes_str += '\n' + item_str
        return str(self.__class__) + '\n' + attributes_str

    def save(self):
        filepath = self.__filepath(self.recognition_id, self.extension)
        self.download(filepath)
        return filepath

    @abstractmethod
    def download(self, dir_path, filename):
        pass

    def __filepath(self, file_name, extension):
        project_root_path = Path(__file__).resolve().parent.parent.parent
        dir_path = f"{project_root_path}/resources/multimedia/{os.environ['SPEECH_ENV']}"
        filename = f"{file_name}.{extension}"
        return f"{dir_path}/{filename}"
