import app
from app import Subtitle
from app import RecognitionLine
from app import Duration
import datetime
from unittest import mock
import os
import pytest


class TestSubtitle:
    FILEPATH = f"{os.getcwd()}/resources/subtitles/test/test_recognition_id-subs.srt"

    def setup_method(self):
        recognition_lines = [
            RecognitionLine("Hello!", Duration(0, 3000)),
            RecognitionLine("My name is Marta", Duration(5000, 8000))
        ]
        self.subtitle = Subtitle(
            'test_recognition_id', recognition_lines, 'ar')

    def teardown_method(self):
        if os.getenv('MONGO_DB'):
            config = app.mongodb_client_configured()
            config['client'].drop_database(config['database'])
        if os.path.exists(TestSubtitle.FILEPATH):
            os.remove(TestSubtitle.FILEPATH)

    def test_save_in_file(self):
        filepath = self.subtitle.save_in_file()
        assert filepath == TestSubtitle.FILEPATH
        with open(filepath, 'r') as file:
            actual_lines = file.read().split("\n")
            expected_lines = [
                "1",
                "00:00:00,000 --> 00:00:03,000",
                "Hello!",
                "",
                "2",
                "00:00:05,000 --> 00:00:08,000",
                "My name is Marta",
                ""
            ]
            assert actual_lines == expected_lines

    def test_save_in_mongodb(self):
        doc_id = self.subtitle.save_in_mongodb(42)
        config = app.mongodb_client_configured()
        document = config['collection'].find_one({'_id': doc_id})
        assert document['resource_id'] == 42
        assert document['lines'] == ['Hello!', 'My name is Marta']
        assert document['language_code'] == 'ar'
        assert type(document['created_at']) == datetime.datetime

    @mock.patch.dict(os.environ, {'SUBS_LOCATION': 'invalid'})
    def test_save_invalid_destination(self):
        with pytest.raises(ValueError) as exception:
            self.subtitle.save_subs(42)
        assert exception.match(r"^Invalid value for ENV var SUBS_LOCATION$")

    def test_str(self):
        expected_string = "<class 'app.models.subtitle.Subtitle'>\n" \
            + "recognition_id = test_recognition_id\n" \
            + "lines = [00:00:00,000;00:00:03,000;Hello!\n00:00:05,000;00:00:08,000;My name is Marta]\n" \
            + "language = ar"
        assert self.subtitle.__str__() == expected_string
