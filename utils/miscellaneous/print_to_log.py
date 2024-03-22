from typing import Optional

import aiofiles
from libs.pretty_utils.miscellaneous.time_and_date import unix_to_strtime

from data import config
from utils.db_api.models import Wallet


async def print_to_log(text: str, color: Optional[str] = '', thread: Optional[str] = None,
                       wallet: Optional[Wallet] = None) -> None:
    printable_text = f'{unix_to_strtime()}'

    if thread:
        printable_text += f' | {thread}'

    if wallet:
        printable_text += f' | {wallet.address}'
        if wallet.name:
            printable_text += f' ({wallet.name})'

    printable_text += f' | {text}'
    print(color + printable_text + config.RESET_ALL)

    try:
        async with aiofiles.open(file=config.LOG_FILE, mode='a', encoding='utf-8') as file:
            await file.write(printable_text + '\n')

    except:
        pass
