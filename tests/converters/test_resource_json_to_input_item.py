import app
import pytest


class TestResourceJSONToInputItem:
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
            attr_value = getattr(input_item, key)
            assert attr_value == params[key]
