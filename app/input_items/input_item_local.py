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

    def __init__(self, *, resource_id, language_code, path):
        """
        Initialize an InputItemLocal object by calling the parent's class constructor.
        Also, set the origin_filepath attribute to the path parameter and the extension attribute to the extension of the file.

        Args:
            resource_id (str): a unique identifier of the resource
            language_code (str): the code of the language of the audio
            path (str): the filepath of the local file
        """
        super().__init__(resource_id=resource_id, language_code=language_code)
        self.origin_filepath = path
        self.extension = os.path.splitext(self.origin_filepath)[1].lstrip('.')

    def download(self, destination_filepath):
        """
        Copy the local file from the origin_filepath to the destination_filepath using the shutil.copyfile function.

        Args:
            destination_filepath (str): the filepath of the destination file.
        """
        shutil.copyfile(self.origin_filepath, destination_filepath)
