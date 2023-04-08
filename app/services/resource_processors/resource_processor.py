from abc import ABC, abstractmethod


class ResourceProcessor(ABC):
    def __init__(self, input_item):
        self.input_item = input_item

    def recognition_id(self):
        return self.input_item.recognition_id

    def response(self, subs_location):
        return {
            'status': 'ok',
            'input_item.recognition_id': self.recognition_id(),
            **subs_location,
        }

    @abstractmethod
    def call(self):
        pass
