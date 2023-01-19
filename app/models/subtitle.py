from datetime import datetime
import os
from pathlib import Path
from ..config_loaders.mongodb_client_configured import mongodb_client_configured


class Subtitle:
    def __init__(self, recognition_id, lines, language):
        self.recognition_id = recognition_id
        self.lines = lines
        self.language = language

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
        It connects to MongoDB and saves the subtitles there.
        '''

        subs_info = {
            'resource_id': resource_id,
            'lines': list(map(lambda recognition_line: recognition_line.text, self.lines)),
            'language_code': self.language,
            'created_at': datetime.utcnow()
        }
        mongodb_config = mongodb_client_configured()
        return mongodb_config['collection'].insert_one(subs_info).inserted_id

    def save_in_file(self):
        '''
        It receives an array of strings and prints it in a file.
        It can be in Arabic.
        It prints each item of the array in a different line.
        '''

        sp_path = Path(__file__).resolve().parent.parent.parent
        subs_dir = f"{sp_path}/resources/subtitles/{os.environ['SPEECH_ENV']}"
        subtitles_path = f"{subs_dir}/{self.recognition_id}-subs.srt"

        with open(subtitles_path, 'w') as file:
            for index, recognition_line in enumerate(self.lines, start=1):
                if index != 1:
                    file.write("\n")
                file.write(f"{index}\n")
                file.write(
                    f"{recognition_line.duration_ts_start_srt()} --> {recognition_line.duration_ts_end_srt()}\n")
                file.write(recognition_line.text + "\n")

        return subtitles_path
