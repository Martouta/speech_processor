import app
import os
import pytest


class TestJSONInputResources:
    def test_json_input_resources(self):
        fixture_example_json_input = f"{os.getcwd()}/tests/fixtures/example_input.json"
        input_resources = app.json_input_resources(fixture_example_json_input)

        assert len(input_resources) == 2

        assert input_resources[0]['id'] == 'id_zWQJqt_D-vo'
        assert input_resources[0]['youtube_reference_id'] == 'zWQJqt_D-vo'
        assert input_resources[0]['language_code'] == 'ar'

        assert input_resources[1]['id'] == 'id_CNHe4qXqsck'
        assert input_resources[1]['youtube_reference_id'] == 'CNHe4qXqsck'
        assert input_resources[1]['language_code'] == 'ar'
