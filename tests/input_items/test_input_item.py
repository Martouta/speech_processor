from fileinput import filename
from app import InputItem
from dataclasses import dataclass


class TestInputItem:
    def test_download(self):
        InputItem.__abstractmethods__ = set()

        @dataclass
        class InputItemDummy(InputItem):
            recognition_id: 1

        dummy = InputItemDummy(recognition_id=1)
        assert dummy.download(dir_path='.', filename='example.txt') == None
