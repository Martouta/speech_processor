from ..input_items.recognizer_data import RecognizerData
from ..input_items.input_item import InputItem
from ..input_items.input_item_hosted import InputItemHosted
from ..input_items.input_item_local import InputItemLocal
from ..input_items.input_item_tiktok import InputItemTiktok
from ..input_items.input_item_youtube import InputItemYoutube

INPUT_TYPE_TO_ITEM_CLASS = {
    'local':  InputItemLocal,
    'hosted': InputItemHosted,
    'tiktok': InputItemTiktok,
    'youtube': InputItemYoutube
}


def resource_json_to_input_item(json: dict) -> InputItem:
    json = json.copy()
    type = json.pop('integration')
    input_item_class = INPUT_TYPE_TO_ITEM_CLASS[type]

    recognizer_data = RecognizerData(**{
        'recognizer': json.pop('recognizer', None),
        'language_code': json.pop('language_code')
    })

    return input_item_class(**json, **{'recognizer_data': recognizer_data})
