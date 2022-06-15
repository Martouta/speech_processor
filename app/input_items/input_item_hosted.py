import requests
from .input_item import InputItem


class InputItemHosted(InputItem):
    def __init__(self, *, resource_id, language_code, url, extension):
        super().__init__(resource_id=resource_id, language_code=language_code)
        self.url = url
        self.extension = extension

    def download(self, filepath):
        response = requests.get(self.url, allow_redirects=True)

        file = open(filepath, 'wb')
        file.write(response.content)
        file.close()
