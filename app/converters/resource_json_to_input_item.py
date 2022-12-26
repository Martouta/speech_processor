from app.input_items.input_item import InputItem
from ..input_items.input_item import InputItem
from ..input_items.input_item_hosted import InputItemHosted
from ..input_items.input_item_local import InputItemLocal
from ..input_items.input_item_tiktok import InputItemTiktok
from ..input_items.input_item_youtube import InputItemYoutube

INPUT_TYPE_TO_ITEM_CLASS = {'local':  InputItemLocal,
                            'hosted': InputItemHosted,
                            'tiktok': InputItemTiktok,
                            'youtube': InputItemYoutube}


def resource_json_to_input_item(json: dict) -> InputItem:
    type = json.pop('integration')
    input_item_class = INPUT_TYPE_TO_ITEM_CLASS[type]
    return input_item_class(**json)
