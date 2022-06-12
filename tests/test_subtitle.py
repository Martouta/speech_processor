import pytest
import app
from app import Subtitle
import datetime
from unittest import mock
import os


class TestSubtitle:
    FILEPATH = f"{os.getcwd()}/subtitles/test/test_recognition_id-subs.txt"

    def setup_method(self):
        self.subtitle = Subtitle('test_recognition_id', ["مرحبا", "إسمي مارتا"], 'ar')

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
            assert file.read().split("\n") == self.subtitle.lines

    def test_save_in_mongodb(self):
        doc_id = self.subtitle.save_in_mongodb(42)
        config = app.mongodb_client_configured()
        document = config['collection'].find_one({'_id': doc_id})
        assert document['resource_id'] == 42
        assert document['lines'] == self.subtitle.lines
        assert document['language_code'] == 'ar'
        assert type(document['created_at']) == datetime.datetime

    @mock.patch.dict(os.environ, {'SUBS_LOCATION': 'invalid'})
    def test_save_invalid_destination(self):
        with pytest.raises(ValueError) as exception:
            self.subtitle.save_subs(42)
        assert exception.match(r"^Invalid value for ENV var SUBS_LOCATION$")
