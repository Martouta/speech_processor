from app.process_resource import process_resource
import re
from unittest import mock


class TestProcessResource:
    RESOURCE_ID = 123456789

    def test_process_resource_correctly(self):
        json_parsed = {
            'integration': 'hosted',
            'url': 'http://localhost/example.mp4',
            'language_code': 'ar',
            'resource_id': TestProcessResource.RESOURCE_ID
        }

        with mock.patch('app.input_items.input_item.InputItem.call_resource_processor') as call_resource_processor_mock:
            call_resource_processor_mock.return_value = {'status': 'ok'}

            processed_resource = process_resource(json_parsed)

        assert 'ok' == processed_resource['status']

    def test_process_resource_error(self, caplog):
        json_parsed = {
            'integration': 'hosted',
            'url': 'http://localhost/example.mp4',
            'language_code': 'ar',
            'resource_id': TestProcessResource.RESOURCE_ID,
        }

        with mock.patch('app.input_items.input_item.InputItem.call_resource_processor') as call_resource_processor_mock:
            call_resource_processor_mock.side_effect = Exception(
                'Processing failed')

            resp = process_resource(json_parsed)

        assert resp['status'] == 'error'
        assert type(resp['error']) == Exception
        assert str(resp['error']) == 'Processing failed'

        assert re.search(r"Traceback", caplog.text, re.MULTILINE)
        assert re.search(r".*File.*line \d+, in process_resource",
                         caplog.text, re.MULTILINE)
        assert re.search('Processing failed', caplog.text, re.MULTILINE)
