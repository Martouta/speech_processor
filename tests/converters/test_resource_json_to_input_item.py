import app
from app.services.google_speech_recognizer import GoogleSpeechRecognizer
import pytest


class TestResourceJSONToInputItem:
    def test_resource_json_to_input_item_hosted(self):
        params = {
            'integration': 'local',
            'url': 'tests/fixtures/example.mp3',
            'resource_id': 42,
            'language_code': 'ar'
        }
        input_item = app.resource_json_to_input_item(params)
        assert type(input_item) == app.InputItemLocal
        self.assert_params(input_item, params)

    def test_resource_json_to_input_item_hosted(self):
        params = {
            'integration': 'hosted',
            'url': 'https://localhost:3000/example.mp4',
            'resource_id': 42,
            'language_code': 'es'
        }
        input_item = app.resource_json_to_input_item(params)
        assert type(input_item) == app.InputItemHosted
        self.assert_params(input_item, params)

    def test_resource_json_to_input_item_tiktok(self):
        params = {
            'integration': 'tiktok',
            'id': '7105531486224370946',
            'resource_id': 42,
            'language_code': 'en'
        }
        input_item = app.resource_json_to_input_item(params)
        assert type(input_item) == app.InputItemTiktok
        self.assert_params(input_item, params)

    def test_resource_json_to_input_item_youtube(self):
        params = {
            'integration': 'youtube',
            'id': 'zWQJqt_D-vo',
            'resource_id': 42,
            'language_code': 'ar'
        }
        input_item = app.resource_json_to_input_item(params)
        assert type(input_item) == app.InputItemYoutube
        self.assert_params(input_item, params)

    def test_resource_json_to_input_item_unsupported(self):
        with pytest.raises(KeyError) as exception:
            app.resource_json_to_input_item({'integration': 'unsupported'})
        assert exception.match(r"^'unsupported'$")

    def assert_params(self, input_item, params):
        for key in params:
            if key == 'language_code':
                input_item.recognizer_data.language_code == params[key] # FIXME: RIP LoD
            elif key == 'recognizer':
                input_item.recognizer_data.recognizer_class == GoogleSpeechRecognizer # FIXME: RIP LoD
            else:
                attr_value = getattr(input_item, key)
                assert attr_value == params[key]
