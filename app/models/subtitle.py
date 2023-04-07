from datetime import datetime
import logging
import os
from pathlib import Path
from ..config_loaders.mongodb_client_configured import mongodb_client_configured


class Subtitle:
    def __init__(self, recognition_id, lines, language):
        self.recognition_id = recognition_id
        self.lines = lines
        self.language = language

    def __eq__(self, other) -> bool:
        if not isinstance(other, Subtitle):
            return False
        return self.recognition_id == other.recognition_id \
            and self.lines == other.lines \
            and self.language == other.language

    def __repr__(self):
        return f"Subtitle(recognition_id='{self.recognition_id}', lines={self.lines}, language='{self.language}')"

    def __str__(self):
        attributes_str = f'recognition_id = {self.recognition_id}\n'
        lines_str = '\n'.join(str(line) for line in self.lines)
        attributes_str += f'lines = [{lines_str}]\n'
        attributes_str += f'language = {self.language}'
        return str(self.__class__) + '\n' + attributes_str

    def save_subs(self, resource_id: int):
        subs_location = os.getenv('SUBS_LOCATION', 'mongodb')
        match os.getenv('SUBS_LOCATION', 'mongodb'):
            case 'mongodb':
                id_location = self.save_in_mongodb(resource_id)
            case 'file':
                id_location = self.save_in_file()
            case _:
                raise ValueError('Invalid value for ENV var SUBS_LOCATION')
        return {'subtitles_location': subs_location, 'id_location': id_location}

    def save_in_mongodb(self, resource_id: int):
        '''
        If there are lines, it connects to MongoDB and saves the subtitles there.
        '''
        if not self.lines:
            logging.getLogger(__name__).info('No lines to save in file')
            return None

        subs_info = {
            'resource_id': resource_id,
            'lines': list(map(lambda recognition_line: recognition_line.to_dict(), self.lines)),
            'language_code': self.language,
            'created_at': datetime.utcnow()
        }
        mongodb_config = mongodb_client_configured()
        return mongodb_config['collection'].insert_one(subs_info).inserted_id

    def save_in_file(self) -> str:
        '''
        If there are lines, it receives an array of strings and prints it in a file.
        It can be in Arabic.
        It prints each item of the array in a different line.
        '''
        if not self.lines:
            logging.getLogger(__name__).info('No lines to save in file')
            return None

        sp_path = Path(__file__).resolve().parent.parent.parent
        subs_dir = f"{sp_path}/resources/subtitles/{os.environ['SPEECH_ENV']}"
        subtitles_path = f"{subs_dir}/{self.recognition_id}-subs.srt"

        with open(subtitles_path, 'w') as file:
            for index, recognition_line in enumerate(self.lines, start=1):
                if index != 1:
                    file.write("\n")
                file.write(f"{index}\n")
                file.write(f"{recognition_line.duration_ts_srt()}\n")
                file.write(f"{recognition_line.text}\n")

        return subtitles_path
