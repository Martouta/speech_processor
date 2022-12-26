from app import InputItemLocal
import tempfile
import os
import shutil
import pytest


class TestInputItemLocal:
    @pytest.fixture
    def temp_dir(self):
        temp_dir = tempfile.TemporaryDirectory()
        yield temp_dir
        temp_dir.cleanup()

    def test_download(self, temp_dir):
        origin_filepath = os.path.join(temp_dir.name, 'origin.txt')
        destination_filepath = os.path.join(temp_dir.name, 'destination.txt')

        with open(origin_filepath, 'w') as f:
            f.write('Hello, World!')

        input_item = InputItemLocal(resource_id=42, language_code='en', path=origin_filepath)
        input_item.download(destination_filepath)

        # Check that the file was copied to the destination
        assert os.path.exists(destination_filepath)

        # Check that the content of the destination file is the same as the origin file
        with open(origin_filepath, 'r') as f:
            origin_content = f.read()
        with open(destination_filepath, 'r') as f:
            destination_content = f.read()
        assert origin_content == destination_content

    @pytest.mark.skip(reason='TODO WIP')
    def test_save(self):
        pass
