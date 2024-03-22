from typing import Union, List, Dict, Any

from openpyxl.reader.excel import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from libs.pretty_utils.miscellaneous.files import join_path


def read_spreadsheet(path: Union[str, tuple, list]) -> List[Dict[str, Any]]:
    path = join_path(path)
    spreadsheet = load_workbook(path)
    sheet: Worksheet = spreadsheet.active
    headers = [cell.value for cell in list(sheet.rows)[0]]
    wallets = []

    for wallet in list(sheet.rows)[1:]:
        wallet = [str(cell.value).strip() for cell in wallet]
        filtered_list = list(filter(lambda x: x, wallet))
        if not filtered_list:
            continue
        wallets.append(dict(zip(headers, wallet)))

    return wallets
