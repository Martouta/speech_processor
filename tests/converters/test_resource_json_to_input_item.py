import app
from app.services.speech_recognizers.google_speech_recognizer import GoogleSpeechRecognizer
import pytest


class TestResourceJSONToInputItem:
    def test_resource_json_to_input_item_local(self):
        params = {
            'integration': 'local',
            'path': 'tests/fixtures/example.mp3',
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
            'language_code': 'es',
            'recognizer': 'gladia'
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
        recognizer = params['recognizer'] if 'recognizer' in params else None
        language_code = params['language_code']
        assert input_item.recognizer_data == app.RecognizerData(
            recognizer=recognizer, language_code=language_code)
        for key in params:
            if key not in ['language_code', 'recognizer', 'integration']:
                if key == 'path':
                    attr_value = getattr(input_item, 'origin_filepath')
                    assert attr_value == params[key]
                else:
                    attr_value = getattr(input_item, key)
                    assert attr_value == params[key]
