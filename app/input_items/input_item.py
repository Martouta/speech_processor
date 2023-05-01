from datetime import datetime
from pathlib import Path
import threading
import os
from abc import ABC, abstractmethod
from app.muted_stdout_stderr import muted_stdout_stderr


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
        with muted_stdout_stderr():
            self.download(filepath)
        return filepath

    def call_resource_processor(self):
        processor_class = self.recognizer_data.processor_class
        return processor_class(self).call()

    def language_code(self):
        return self.recognizer_data.language_code

    @abstractmethod
    def download(self, filename):
        pass

    def __filepath(self, file_name, extension):
        project_root_path = Path(__file__).resolve().parent.parent.parent
        dir_path = f"{project_root_path}/resources/multimedia/{os.environ['SPEECH_ENV']}"
        filename = f"{file_name}.{extension}"
        return f"{dir_path}/{filename}"
