import pytest
import app
from app import Subtitle
import datetime
import os


class TestSubtitle:
    FILEPATH = f"{os.getcwd()}/subtitles/test/test_recognition_id-subs.txt"

    def teardown_method(self):
        config = app.mongodb_client_configured()
        config['client'].drop_database(config['database'])
        if os.path.exists(TestSubtitle.FILEPATH):
            os.remove(TestSubtitle.FILEPATH)

    def test_save_in_file(self):
        lines = ["مرحبا", "إسمي مارتا"]
        subtitle = Subtitle('test_recognition_id', lines, 'ar')
        filepath = subtitle.save_in_file()
        assert filepath == TestSubtitle.FILEPATH
        with open(filepath, 'r') as file:
            assert file.read().split("\n") == lines

    def test_save_in_mongodb(self):
        lines = ["مرحبا", "إسمي مارتا"]
        subtitle = Subtitle('test_recognition_id', lines, 'ar')
        doc_id = subtitle.save_in_mongodb('42')
        config = app.mongodb_client_configured()
        document = config['collection'].find_one({'_id': doc_id})
        assert document['resource_id'] == 42
        assert document['lines'] == lines
        assert document['language_code'] == 'ar'
        assert type(document['created_at']) == datetime.datetime
