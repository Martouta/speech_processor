from datetime import datetime
import os
from pathlib import Path
from .mongodb_client_configured import mongodb_client_configured


class Subtitle:
    def __init__(self, recognition_id, lines, language):
        self.recognition_id = recognition_id
        self.lines = lines
        self.language = language

    def __str__(self):
        attributes_str = ''
        for item in self.__dict__:
            item_str = '{} = {}'.format(item, self.__dict__[item])
            attributes_str += '\n' + item_str
        return str(self.__class__) + '\n' + attributes_str

    def save_subs(self, resource_id):
        subs_location = os.getenv('SUBS_LOCATION', 'mongodb')
        match os.getenv('SUBS_LOCATION', 'mongodb'):
            case 'mongodb':
                id_location = self.save_in_mongodb(resource_id)
            case 'file':
                id_location = self.save_in_file()
            case _:
                raise ValueError('Invalid value for ENV var SUBS_LOCATION')
        return {'subtitles_location': subs_location, 'id_location': id_location}

    def save_in_mongodb(self, resource_id):
        '''
        It connects to MongoDB and saves the subtitles there.
        '''

        subs_info = {
            'resource_id': int(resource_id),
            'lines': self.lines,
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

        sp_path = Path(__file__).resolve().parent.parent
        subs_dir = f"{sp_path}/subtitles/{os.environ['SPEECH_ENV']}"
        subtitles_path = f"{subs_dir}/{self.recognition_id}-subs.txt"

        with open(subtitles_path, 'w') as file:
            for index, line in enumerate(self.lines):
                if index != 0:
                    file.write("\n")
                file.write(line)

        return subtitles_path
