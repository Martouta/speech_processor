import app
from app import ResourceAudio
import os
import pytest
import shutil


class TestCleanupTemporaryFiles:
    VIDEO_FIXTURE_FILE_PATH = f"{os.getcwd()}/tests/fixtures/example.mp4"

    def test_cleanup_temporary_files_when_they_exist_for_video_mp4(self):
        self.assert_cleanup_temporary_files_when_they_exist('mp4')

    def test_cleanup_temporary_files_when_they_exist_for_audio_mp3(self):
        self.assert_cleanup_temporary_files_when_they_exist('mp3')

    def test_cleanup_temporary_files_when_they_exist_for_audio_wav(self):
        self.assert_cleanup_temporary_files_when_they_exist('wav')

    def test_cleanup_temporary_files_when_they_do_not_exist(self):
        recognition_id = 'recognition_id'
        multimedia_name = f"{recognition_id}-example.wav"

        downloaded_multimedia_path = f"{os.getcwd()}/audios/test/{multimedia_name}"
        audio_chunks_path = f"{os.getcwd()}/audio_chunks/test/{recognition_id}"

        app.cleanup_temporary_files(recognition_id, downloaded_multimedia_path)
        assert os.path.exists(downloaded_multimedia_path) == False
        assert os.path.exists(audio_chunks_path) == False

    def assert_cleanup_temporary_files_when_they_exist(self, format):
        recognition_id = 'recognition_id'
        multimedia_name = f"{recognition_id}-example"
        resource_type = 'video'
        if format != 'mp4':
            resource_type = 'audio'

        downloaded_multimedia_path = f"{os.getcwd()}/{resource_type}s/test/{multimedia_name}.{format}"
        shutil.copyfile(
            TestCleanupTemporaryFiles.VIDEO_FIXTURE_FILE_PATH, downloaded_multimedia_path)
        assert os.path.exists(downloaded_multimedia_path)

        ResourceAudio.save_as_wav(recognition_id, downloaded_multimedia_path)
        generated_audio_path = f"{os.getcwd()}/audios/test/{multimedia_name}.wav"
        assert os.path.exists(generated_audio_path)

        audio_chunks_path = f"{os.getcwd()}/audio_chunks/test/{recognition_id}"
        self.create_folder(audio_chunks_path)
        os.path.exists(audio_chunks_path)

        app.cleanup_temporary_files(recognition_id, downloaded_multimedia_path)
        assert os.path.exists(downloaded_multimedia_path) == False
        assert os.path.exists(generated_audio_path) == False
        assert os.path.exists(audio_chunks_path) == False

    def create_folder(self, path):
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
