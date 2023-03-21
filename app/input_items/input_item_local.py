import os
import shutil
from .input_item import InputItem


class InputItemLocal(InputItem):
    """
    A class representing a local input item. 
    It inherits from the InputItem class and extends it by adding a path attribute that stores the filepath of the local file.

    Attributes:
        resource_id (str): a unique identifier of the resource
        language_code (str): the code of the language of the audio
        origin_filepath (str): the filepath of the local file
        extension (str): the extension of the file
    """

    def __init__(self, *, resource_id, recognizer_data, path):
        """Initialize the object.
    
        Arguments:
            resource_id: The ID of the resource.
            language_code: The BCP-47 language code to use for speech recognition.
            recognizer: The speech recognition engine to use.
            path: The path to the audio file to be transcribed.
        """
        super().__init__(
            resource_id=resource_id,
            recognizer_data=recognizer_data
        )
        self.origin_filepath = path
        self.extension = os.path.splitext(self.origin_filepath)[1].lstrip('.')

    def download(self, destination_filepath):
        """
        Copy the local file from the origin_filepath to the destination_filepath using the shutil.copyfile function.

        Args:
            destination_filepath (str): the filepath of the destination file.
        """
        shutil.copyfile(self.origin_filepath, destination_filepath)
