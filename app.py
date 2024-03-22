import os
import sys
import asyncio
import getpass

from loguru import logger
from utils.miscellaneous.create_files import create_files

from data import config
from functions.Export import Export

from functions.Import import Import

from functions.activity import activity
from utils.encryption import get_cipher_suite
from data.config import SALT_PATH, CIPHER_SUITE
from data.models import ProgramActions, Settings

from utils.user_menu import get_action
from utils.db_api.database import get_wallets
from utils.adjust_policy import set_windows_event_loop_policy


def check_encrypt_param(settings):
    if settings.use_private_key_encryption:
        if not os.path.exists(SALT_PATH):
            print(f'You need to add salt.dat to {SALT_PATH} for correct decryption of private keys!\n'
                  f'After the program has started successfully, you can delete this file. \n\n'
                  f'If you do not need encryption, please change use_private_key_encryption to False.')
            sys.exit(1)
        with open(SALT_PATH, 'rb') as f:
            salt = f.read()
        user_password = getpass.getpass('[DECRYPTOR] Write here you password '
                                        '(the field will be hidden): ').strip().encode()
        CIPHER_SUITE.append(get_cipher_suite(user_password, salt))


async def start_script():
    wallets = get_wallets()
    settings = Settings()

    if not settings.oklink_api_key:
        logger.error('Specify the API key for Oklink.com!')
        return

    if not wallets:
        logger.error('Вы не добавили кошельки в бд!')
        return

    await asyncio.wait([
        asyncio.create_task(activity())
    ])


def print_logo():
    print("""\

     █████╗ ██████╗ ██████╗ ██╗   ██╗███████╗███████╗██████╗ ███████╗
    ██╔══██╗██╔══██╗██╔══██╗██║   ██║╚══███╔╝██╔════╝██╔══██╗██╔════╝
    ███████║██████╔╝██████╔╝██║   ██║  ███╔╝ █████╗  ██████╔╝███████╗
    ██╔══██║██╔══██╗██╔══██╗██║   ██║ ███╔╝  ██╔══╝  ██╔══██╗╚════██║
    ██║  ██║██║  ██║██████╔╝╚██████╔╝███████╗███████╗██║  ██║███████║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝
    """)

if __name__ == '__main__':
    create_files()
    print_logo()
    set_windows_event_loop_policy()
    main_settings = Settings()
    check_encrypt_param(main_settings)
    loop = asyncio.new_event_loop()

    try:

        action = get_action()

        match action:

            # Импорт
            case ProgramActions.ImportWallets.Selection:
                asyncio.run(Import.wallets())

            # Экспорт 
            case ProgramActions.ExportWallets.Selection:
                asyncio.run(Export.wallets())

            # Запуск основных действий
            case ProgramActions.StartScript.Selection:
                asyncio.run(start_script())

    except (KeyboardInterrupt, TypeError):
        print()
        logger.info('Программа завершена')
        print()
        sys.exit(1)

    except ValueError as err:
        print(f"{config.RED}Value error: {err}{config.RESET_ALL}")

    except BaseException as e:
        logger.error('main')
        print(f'\n{config.RED}Something went wrong: {e}{config.RESET_ALL}\n')

    if action and action != ProgramActions.StartScript:
        input(f'\nPress {config.LIGHTGREEN_EX}Enter{config.RESET_ALL} to exit.\n')
