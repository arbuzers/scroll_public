import os
import sys
import platform
from pathlib import Path

import asyncio

from loguru import logger
from colorama import Fore, Style


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()

else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

if platform.system() == 'Windows':
    GREEN = ''
    LIGHTGREEN_EX = ''
    RED = ''
    BLUE = ''
    RESET_ALL = ''

else:
    GREEN = Fore.GREEN
    LIGHTGREEN_EX = Fore.LIGHTGREEN_EX
    RED = Fore.RED
    BLUE = Fore.BLUE
    RESET_ALL = Style.RESET_ALL

FILES_DIR = os.path.join(ROOT_DIR, 'files')
ABIS_DIR = os.path.join(ROOT_DIR, 'data', 'abis')

SALT_PATH = os.path.join(FILES_DIR, 'salt.dat')
WALLETS_DB = os.path.join(FILES_DIR, 'wallets.db')

LOG_FILE = os.path.join(FILES_DIR, 'log.log')
ERRORS_FILE = os.path.join(FILES_DIR, 'errors.log')

EXPORT_FILE = os.path.join(FILES_DIR, 'export.xlsx')
IMPORT_FILE = os.path.join(FILES_DIR, 'import.xlsx')
PROXIES_FILE = os.path.join(FILES_DIR, 'proxies.txt')
SETTINGS_FILE = os.path.join(FILES_DIR, 'settings.json')
BALANCE = os.path.join(FILES_DIR, 'eth_balance_result.json')


CIPHER_SUITE = []

# logger.remove()
logger.add(f'{FILES_DIR}/debug.log', format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}', level='DEBUG')

semaphore = asyncio.Semaphore(100)
lock = asyncio.Lock()
