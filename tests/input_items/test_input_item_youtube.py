import glob
import os
from app.input_items.input_item_youtube import InputItemYoutube
from app.input_items.recognizer_data import RecognizerData
import re
from unittest.mock import patch, call


class TestInputItemYoutube:
    def teardown_method(self):
        for fname in glob.glob('resources/multimedia/test/*.mp4'):
            os.remove(fname)

    def test_save(self):
        filepath = self.submit_save_request('zWQJqt_D-vo')
        expected_filepath_regexp = r'^' + re.escape(f"{os.getcwd()}/") \
            + re.escape('resources/multimedia/test/') \
            + r'\d+-55-' \
            + r'\d{2}-\d{2}\.\d{2}:\d{2}:\d+\.mp4$'
        assert re.match(expected_filepath_regexp, filepath)

    def submit_save_request(self, id):
        with patch('yt_dlp.YoutubeDL') as mock_youtube_dl:
            mock_youtube_dl.return_value.download.return_value = None
            item = InputItemYoutube(id=id, recognizer_data=RecognizerData(
                language_code='en'), resource_id=55)
            filepath = item.save()

            options = {
                'format': 'worstvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'outtmpl': filepath,
            }
            mock_youtube_dl.assert_called_once_with(options)
            mock_youtube_dl.return_value.__enter__.return_value.download.assert_called_once_with(
                ['https://www.youtube.com/watch?v=zWQJqt_D-vo']
            )

        return filepath
