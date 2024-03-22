from typing import Optional

from libs.pretty_utils.type_functions.dicts import update_dict
from libs.pretty_utils.miscellaneous.files import touch, write_json, read_json

from data import config
from utils.miscellaneous.create_spreadsheet import create_spreadsheet


def create_files():
    touch(path=config.FILES_DIR)
    create_spreadsheet(path=config.IMPORT_FILE, headers=('private_key', 'name', 'proxy'),
                       sheet_name='Wallets')

    try:
        current_settings: Optional[dict] = read_json(path=config.SETTINGS_FILE)

    except:
        current_settings = {}

    settings = {
        'use_private_key_encryption': False,
        'maximum_gas_price': 50,
        'oklink_api_key': '',
        'networks': {
            # Добавляем пул рпц для актуальной сети
            'Scroll': {'rpcs': ['https://rpc.ankr.com/scroll']},
        },
        'minimal_balance': 0.0014,
        'activity_actions_delay': {'from': 86400, 'to': 864000},

        'dmail': {'from': 5, 'to': 15},
        'mint_nft': {'from': 5, 'to': 15},
        'votes': {'from': 5, 'to': 15},
    }
    write_json(path=config.SETTINGS_FILE, obj=update_dict(modifiable=current_settings, template=settings), indent=2)


create_files()
