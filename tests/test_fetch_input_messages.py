import app
import os
from unittest import mock


class TestFetchInputMessages:
    INPUT_FILE = f"{os.getcwd()}/tests/fixtures/example_input.json"

    @mock.patch.dict(os.environ, {'INPUT_FILE': INPUT_FILE})
    def test_fetch_input_msgs_from_input_file(self):
        messages = app.fetch_input_messages()

        assert len(messages) == 5

        assert messages[0]['type'] == 'youtube'
        assert messages[0]['id'] == 'zWQJqt_D-vo'
        assert messages[0]['language_code'] == 'ar'
        assert messages[0]['resource_id'] == 1

        assert messages[1]['type'] == 'youtube'
        assert messages[1]['id'] == 'CNHe4qXqsck'
        assert messages[1]['language_code'] == 'ar'
        assert messages[1]['resource_id'] == 2

        assert messages[2]['type'] == 'tiktok'
        assert messages[2]['id'] == '7105531486224370946'
        assert messages[2]['language_code'] == 'en-au'
        assert messages[2]['resource_id'] == 3

        assert messages[3]['type'] == 'hosted'
        assert messages[3]['url'] == 'https://scontent-mad1-1.cdninstagram.com/v/t50.16885-16/286327419_404827821544713_6636671397284152039_n.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InZ0c192b2RfdXJsZ2VuLjcyMC5pZ3R2LmJhc2VsaW5lIiwicWVfZ3JvdXBzIjoiW1wiaWdfd2ViX2RlbGl2ZXJ5X3Z0c19vdGZcIl0ifQ&_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=109&_nc_ohc=FGWru4cNdLMAX_K4E5b&tn=VRHGuwVQgXScv-7F&edm=ALQROFkBAAAA&vs=546391373741490_1076324468&_nc_vs=HBksFQAYJEdIc0NFUkVKbFg5U01IQUJBT2NDSGlaNU1ScGNidlZCQUFBRhUAAsgBABUAGCRHRUgyQmhHSURDbDNpUWNDQUp2ODkxY04wS1puYnZWQkFBQUYVAgLIAQAoABgAGwGIB3VzZV9vaWwBMRUAACb6%2BOSmwr7VPxUCKAJDMywXQDiAAAAAAAAYEmRhc2hfYmFzZWxpbmVfMV92MREAdewHAA%3D%3D&ccb=7-5&oe=62A764B0&oh=00_AT_IQEa1RZ7hMDzWS9a5mvRrO09DPi_K8AqXglaNuP7JEg&_nc_sid=30a2ef'
        assert messages[3]['language_code'] == 'en-US'
        assert messages[3]['resource_id'] == 4

        assert messages[4]['type'] == 'hosted'
        assert messages[4]['url'] == 'https://file-examples.com/storage/fece7372cf62a47bc9626b9/2017/11/file_example_MP3_700KB.mp3'
        assert messages[4]['language_code'] == 'en-US'
        assert messages[4]['resource_id'] == 5

    def test_fetch_input_msgs_from_kafka(self):
        messages = app.fetch_input_messages()
        assert type(messages) == type(app.kafka_consumer_configured())
