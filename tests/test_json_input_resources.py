import app
import os
import pytest


class TestJSONInputResources:
    def test_json_input_resources(self):
        fixture_example_json_input = f"{os.getcwd()}/tests/fixtures/example_input.json"
        input_resources = app.json_input_resources(fixture_example_json_input)

        assert len(input_resources) == 5

        assert input_resources[0]['type'] == 'youtube'
        assert input_resources[0]['id'] == 'zWQJqt_D-vo'
        assert input_resources[0]['language_code'] == 'ar'
        assert input_resources[0]['resource_id'] == 1

        assert input_resources[1]['type'] == 'youtube'
        assert input_resources[1]['id'] == 'CNHe4qXqsck'
        assert input_resources[1]['language_code'] == 'ar'
        assert input_resources[1]['resource_id'] == 2

        assert input_resources[2]['type'] == 'tiktok'
        assert input_resources[2]['id'] == '7105531486224370946'
        assert input_resources[2]['language_code'] == 'en-au'
        assert input_resources[2]['resource_id'] == 3

        assert input_resources[3]['type'] == 'hosted_video'
        assert input_resources[3]['url'] == 'https://scontent-mad1-1.cdninstagram.com/v/t50.16885-16/286327419_404827821544713_6636671397284152039_n.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InZ0c192b2RfdXJsZ2VuLjcyMC5pZ3R2LmJhc2VsaW5lIiwicWVfZ3JvdXBzIjoiW1wiaWdfd2ViX2RlbGl2ZXJ5X3Z0c19vdGZcIl0ifQ&_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=109&_nc_ohc=FGWru4cNdLMAX_K4E5b&tn=VRHGuwVQgXScv-7F&edm=ALQROFkBAAAA&vs=546391373741490_1076324468&_nc_vs=HBksFQAYJEdIc0NFUkVKbFg5U01IQUJBT2NDSGlaNU1ScGNidlZCQUFBRhUAAsgBABUAGCRHRUgyQmhHSURDbDNpUWNDQUp2ODkxY04wS1puYnZWQkFBQUYVAgLIAQAoABgAGwGIB3VzZV9vaWwBMRUAACb6%2BOSmwr7VPxUCKAJDMywXQDiAAAAAAAAYEmRhc2hfYmFzZWxpbmVfMV92MREAdewHAA%3D%3D&ccb=7-5&oe=62A764B0&oh=00_AT_IQEa1RZ7hMDzWS9a5mvRrO09DPi_K8AqXglaNuP7JEg&_nc_sid=30a2ef'
        assert input_resources[3]['filename'] == 'example_mp4'
        assert input_resources[3]['language_code'] == 'en-US'
        assert input_resources[3]['resource_id'] == 4

        assert input_resources[4]['type'] == 'hosted_audio'
        assert input_resources[4]['url'] == 'https://file-examples.com/storage/fece7372cf62a47bc9626b9/2017/11/file_example_MP3_700KB.mp3'
        assert input_resources[4]['filename'] == 'example_mp3'
        assert input_resources[4]['language_code'] == 'en-US'
        assert input_resources[4]['resource_id'] == 5
