import re
import requests
from .input_item import InputItem


class InputItemHosted(InputItem):
    def __init__(self, *, resource_id, language_code, url):
        super().__init__(resource_id=resource_id, language_code=language_code)
        self.url = url
        self.extension = self.extension_from_url()

    def download(self, filepath):
        response = requests.get(self.url, allow_redirects=True)

        file = open(filepath, 'wb')
        file.write(response.content)
        file.close()

    def extension_from_url(self) -> str:
        match = re.search(r"\.(mp4|mp3|wav)", self.url, re.IGNORECASE)
        if match:
            return match.group(1)
        return ''
