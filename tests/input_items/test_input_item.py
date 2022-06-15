from fileinput import filename
from multiprocessing import dummy
from app import InputItem
from dataclasses import dataclass


class TestInputItem:
    InputItem.__abstractmethods__ = set()

    @dataclass
    class InputItemDummy(InputItem):
        recognition_id: 1

    def test_download(self):
        dummy = TestInputItem.InputItemDummy(recognition_id=1)
        assert dummy.download(dir_path='.', filename='example.txt') == None

    def test_str(self):
        dummy = TestInputItem.InputItemDummy(recognition_id=1)
        dummy_string = dummy.__str__()
        assert dummy_string == "<class 'test_input_item.TestInputItem.InputItemDummy'>\n\nrecognition_id = 1"
