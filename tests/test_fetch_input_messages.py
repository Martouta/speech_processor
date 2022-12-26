import app
import os
from unittest import mock


class TestFetchInputMessages:
    INPUT_FILE = f"{os.getcwd()}/tests/fixtures/example_input.json"

    @mock.patch.dict(os.environ, {'INPUT_FILE': INPUT_FILE})
    def test_fetch_input_msgs_from_input_file(self):
        messages = app.fetch_input_messages()

        assert messages[0]['integration'] == 'youtube'
        assert messages[0]['id'] == 'zWQJqt_D-vo'
        assert messages[0]['language_code'] == 'ar'
        assert messages[0]['resource_id'] == 1

        assert messages[1]['integration'] == 'youtube'
        assert messages[1]['id'] == 'CNHe4qXqsck'
        assert messages[1]['language_code'] == 'ar'
        assert messages[1]['resource_id'] == 2

        assert messages[2]['integration'] == 'tiktok'
        assert messages[2]['id'] == '7105531486224370946'
        assert messages[2]['language_code'] == 'en-au'
        assert messages[2]['resource_id'] == 3

        assert messages[3]['integration'] == 'hosted'
        assert messages[3]['url'] == 'https://scontent-mad1-1.cdninstagram.com/v/t50.16885-16/10000000_4897336923689152_6953647669213471758_n.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InZ0c192b2RfdXJsZ2VuLjEyODAuaWd0di5iYXNlbGluZSIsInFlX2dyb3VwcyI6IltcImlnX3dlYl9kZWxpdmVyeV92dHNfb3RmXCJdIn0&_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=104&_nc_ohc=OfiUjon4e6AAX8fa1iX&edm=ALQROFkBAAAA&vs=504042498033080_1629363706&_nc_vs=HBksFQAYJEdJQ1dtQURBa0s0YkdtWVJBQTRrc1pDMlVZQmdidlZCQUFBRhUAAsgBABUAGCRHSS1IaXhDdlJKbUlTdHdLQUNYaDgzbUpqb1JWYnZWQkFBQUYVAgLIAQAoABgAGwGIB3VzZV9vaWwBMRUAACbwmrGErMDmPxUCKAJDMywXQFeRBiTdLxsYEmRhc2hfYmFzZWxpbmVfMV92MREAdewHAA%3D%3D&ccb=7-5&oe=62AC1A5F&oh=00_AT9ijqEfW1SCDHUqt3KK79FNnZmlzE9lqGMEegg35y58VQ&_nc_sid=30a2ef'
        assert messages[3]['language_code'] == 'en-US'
        assert messages[3]['resource_id'] == 4

        assert messages[4]['integration'] == 'hosted'
        assert messages[4]['url'] == 'https://lang_src.s3.amazonaws.com/7a.mp3'
        assert messages[4]['language_code'] == 'en-US'
        assert messages[4]['resource_id'] == 5

        assert messages[5]['integration'] == 'local'
        assert messages[5]['path'] == 'tests/fixtures/example.mp3'
        assert messages[5]['language_code'] == 'ar'
        assert messages[5]['resource_id'] == 6

    def test_fetch_input_msgs_from_kafka(self):
        messages = app.fetch_input_messages()
        assert type(messages) == type(app.kafka_consumer_configured())
