import app
import httpretty
import requests
import requests_mock
import re
import glob
import os
import shutil
from datetime import datetime
from unittest import mock


class TestProcessResource:
    RESOURCE_ID = 123456789

    def teardown_method(self):
        config = app.mongodb_client_configured()
        config['client'].drop_database(config['database'])
        audio_chunks_root_dir = f"{os.getcwd()}/resources/audio_chunks/test/"
        audio_chunks_dir_pattern = str(TestProcessResource.RESOURCE_ID) + r".*"
        for dir in os.listdir(audio_chunks_root_dir):
            if (re.search(audio_chunks_dir_pattern, dir)):
                shutil.rmtree(audio_chunks_root_dir + dir)
        for fname in glob.glob('resources/multimedia/test/*.mp4'):
            os.remove(fname)
        for fname in glob.glob('resources/multimedia/test/*.wav'):
            os.remove(fname)
        for fname in glob.glob('resources/subtitles/test/*.txt'):
            os.remove(fname)

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_process_resource_ia_correctly(self):
        api_url = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang=ar&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
        httpretty.register_uri(
            httpretty.POST,
            api_url,
            adding_headers={
                'content-type': 'audio/x-flac; rate=44100'
            },
            responses=[
                httpretty.Response(
                    '{"result":[{"alternative":[{"transcript":"بخير وانت","confidence":0.85492837}],"final":true}],"result_index":0}'),
                httpretty.Response(
                    '{"result":[{"alternative":[{"transcript":"شكرا","confidence":0.5705713}],"final":true}],"result_index":0}')
            ]
        )

        mongodb_config = app.mongodb_client_configured()
        fname, ext = ('example', 'mp4')
        resource_url = f"http://localhost/{fname}.{ext}"
        json_parsed = {
            'integration': 'hosted',
            'url': resource_url,
            'language_code': 'ar',
            'resource_id': TestProcessResource.RESOURCE_ID
        }

        processed_resource = {}
        with requests_mock.Mocker() as req_mock:
            with open(f"{os.getcwd()}/tests/fixtures/{fname}.{ext}", 'rb') as vfile:
                req_mock.get(resource_url, body=vfile)
                processed_resource = app.process_resource(json_parsed)

        assert 'ok' == processed_resource['status']
        assert 'mongodb' == processed_resource['subtitles_location']
        doc_id = processed_resource['id_location']
        doc = mongodb_config['collection'].find_one({'_id': doc_id})
        assert json_parsed['resource_id'] == doc['resource_id']
        expected_recognition_id_regex = r"\d+" \
            + '-' \
            + str(TestProcessResource.RESOURCE_ID) \
            + '-' \
            + datetime.utcnow().strftime('%m-%d.%H') \
            + r":\d{2}:\d{8}"
        assert re.match(expected_recognition_id_regex,
                        processed_resource['input_item.recognition_id'])
        expected_recognition = [
            {'timestamp': '00:00:00,000 --> 00:00:01,328', 'text': 'بخير وانت'},
            {'timestamp': '00:00:01,328 --> 00:00:01,928', 'text': 'شكرا'}
        ]
        assert doc['lines'] == expected_recognition

    @httpretty.activate(verbose=True, allow_net_connect=False)
    @mock.patch.dict(os.environ, {'SUBS_LOCATION': 'file'})
    def test_process_resource_ia_save_in_file(self):
        api_url = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang=ar&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
        httpretty.register_uri(
            httpretty.POST,
            api_url,
            adding_headers={
                'content-type': 'audio/x-flac; rate=44100'
            },
            responses=[
                httpretty.Response(
                    '{"result":[{"alternative":[{"transcript":"بخير وانت","confidence":0.85492837}],"final":true}],"result_index":0}'),
                httpretty.Response(
                    '{"result":[{"alternative":[{"transcript":"شكرا","confidence":0.5705713}],"final":true}],"result_index":0}')
            ]
        )

        fname, ext = ('example', 'mp4')
        resource_url = f"http://localhost/{fname}.{ext}"
        json_parsed = {
            'integration': 'hosted',
            'url': resource_url,
            'language_code': 'ar',
            'resource_id': TestProcessResource.RESOURCE_ID
        }

        processed_resource = {}
        with requests_mock.Mocker() as req_mock:
            with open(f"{os.getcwd()}/tests/fixtures/{fname}.{ext}", 'rb') as vfile:
                req_mock.get(resource_url, body=vfile)
                processed_resource = app.process_resource(json_parsed)

        assert 'ok' == processed_resource['status']
        assert 'file' == processed_resource['subtitles_location']
        expected_subs_path_regex = f"{os.getcwd()}/resources/subtitles/test/" \
            + r"\d+" \
            + '-' \
            + str(TestProcessResource.RESOURCE_ID) \
            + '-' \
            + datetime.utcnow().strftime('%m-%d.%H') \
            + r":\d{2}:\d{8}" \
            + '-' \
            + 'subs.srt'
        assert re.match(expected_subs_path_regex,
                        processed_resource['id_location'])
        with open(processed_resource['id_location'], 'r') as subfile:
            expected_recognition = [
                '1',
                '00:00:00,000 --> 00:00:01,328',
                'بخير وانت',
                '',
                '2',
                '00:00:01,328 --> 00:00:01,928',
                'شكرا',
                ''
            ]
            assert subfile.read().split("\n") == expected_recognition

    def test_process_resource_ia_error(self, caplog):
        resource_url = 'http://localhost/example.mp4'
        json_parsed = {
            'integration': 'hosted',
            'url': resource_url,
            'language_code': 'ar',
            'resource_id': 42
        }

        with requests_mock.Mocker() as req_mock:
            req_mock.get(resource_url,
                         exc=requests.exceptions.ConnectTimeout)
            resp = app.process_resource(json_parsed)
            assert resp['status'] == 'error'
            assert type(resp['error']) == requests.exceptions.ConnectTimeout

            assert re.search(r"Traceback", caplog.text, re.MULTILINE)
            assert re.search(
                r".*File.*line \d+, in process_resource", caplog.text, re.MULTILINE)
            assert re.search(
                re.escape('requests.exceptions.ConnectTimeout'), caplog.text, re.MULTILINE)

    def test_process_resource_captions_correctly(self):
        video_id = 'zWQJqt_D-vo'
        json_parsed = {
            'integration': 'youtube',
            'id': video_id,
            'language_code': 'ar',
            'resource_id': TestProcessResource.RESOURCE_ID,
            'captions': True
        }

        with requests_mock.Mocker() as req_mock:
            with mock.patch('app.YoutubeCaptionsFetcher.call') as fetch_captions_mock:
                lines = [
                    app.RecognitionLine(line_text='بخير وانت', duration=app.Duration(
                        ts_start=0, ts_end=1328)),
                    app.RecognitionLine(line_text='شكرا', duration=app.Duration(
                        ts_start=1328, ts_end=1928))
                ]
                fetch_captions_mock.return_value = app.Subtitle(
                    recognition_id=1, language='ar', lines=lines)
                processed_resource = app.process_resource(json_parsed)

        assert 'ok' == processed_resource['status']
        assert 'mongodb' == processed_resource['subtitles_location']
        mongodb_config = app.mongodb_client_configured()
        doc_id = processed_resource['id_location']
        doc = mongodb_config['collection'].find_one({'_id': doc_id})
        assert json_parsed['resource_id'] == doc['resource_id']
        expected_recognition = [
            {'timestamp': '00:00:00,000 --> 00:00:01,328', 'text': 'بخير وانت'},
            {'timestamp': '00:00:01,328 --> 00:00:01,928', 'text': 'شكرا'}
        ]
        assert doc['lines'] == expected_recognition

    def test_process_resource_captions_error(self, caplog):
        video_id = 'zWQJqt_D-vo'
        json_parsed = {
            'integration': 'youtube',
            'id': video_id,
            'language_code': 'ar',
            'resource_id': TestProcessResource.RESOURCE_ID,
            'captions': True
        }

        with mock.patch('app.YoutubeCaptionsFetcher.call') as fetch_captions_mock:
            fetch_captions_mock.side_effect = Exception('Captions fetch failed')
            resp = app.process_resource(json_parsed)

        assert resp['status'] == 'error'
        assert type(resp['error']) == Exception
        assert str(resp['error']) == "Captions fetch failed"

        assert re.search(r"Traceback", caplog.text, re.MULTILINE)
        assert re.search(r".*File.*line \d+, in process_resource",
                         caplog.text, re.MULTILINE)
        assert re.search(re.escape('Captions fetch failed'),
                         caplog.text, re.MULTILINE)
