import re
import sys
import random
from loguru import logger

from libs.py_eth_async.client import Client

from data import config
from data.models import Settings
from utils.db_api.models import Wallet

from libs.py_eth_async.data.models import Networks

from utils.encryption import get_private_key
from utils.db_api.database import get_wallet, db
from utils.miscellaneous.read_spreadsheet import read_spreadsheet


class Import:
    @staticmethod
    async def wallets() -> None:
        print(f'''Open and fill in the spreadsheet called {config.LIGHTGREEN_EX}import.xlsx{config.RESET_ALL}.\n''')
        input(f'Then press {config.LIGHTGREEN_EX}Enter{config.RESET_ALL}.')
        wallets = read_spreadsheet(path=config.IMPORT_FILE)

        if wallets:
            settings = Settings()
            imported = []
            edited = []
            total = len(wallets)
            sys_exit = False

            for num, wallet in enumerate(wallets):
                logger.info(f'Importing {num+1} out of {len(wallets)} accounts!')
                try:
                    private_key = get_private_key(wallet['private_key'])
                    name = wallet['name']
                    name = str(name) if name else None
                    proxy = wallet['proxy']
                    # mail_data = wallet['mail_data']

                    if 'wrong password or salt' in private_key:
                        logger.error(f'Wrong password or salt! Decrypt private key not possible')
                        sys_exit = True
                        break

                    if not all((private_key,)):
                        print(
                            f"{config.RED}You didn't specify one or more of the mandatory values: "
                            f"private_key!{config.RESET_ALL}"
                        )
                        continue

                    if re.match(r'\w' * 64, private_key):
                        wallet_instance = get_wallet(private_key=private_key)

                        if wallet_instance and wallet_instance.name != name:
                            wallet_instance.name = name
                            db.commit()
                            edited.append(wallet_instance)

                        elif not wallet_instance:
                            client = Client(private_key=private_key, network=Networks.Ethereum)
                            address = client.account.address
                            mint_nft = random.randint(settings.mint_nft.from_, settings.mint_nft.to_)
                            dmail = random.randint(settings.dmail.from_, settings.dmail.to_)
                            votes = random.randint(settings.votes.from_, settings.votes.to_)
                            wallet_instance = Wallet(
                                private_key=wallet['private_key'], address=address, name=name,
                                proxy=proxy, mint_nft=mint_nft, dmail=dmail, votes=votes)
                            db.insert(wallet_instance)
                            imported.append(wallet_instance)

                except:
                    logger.error('Import.wallets')
                    print(f'{config.RED}Failed to import wallet!{config.RESET_ALL}')

            if sys_exit:
                sys.exit(1)

            text = ''
            if imported:
                text += (f'\n--- Imported\n№\t{"address":<72}{"name":<16}{"dmail":<10}{"shit_nft":<10}{"vote":<10}')
                for i, wallet in enumerate(imported):
                    text += (
                        f'\n{i + 1:<2}\t{wallet.address:<72}{wallet.name:<18}{wallet.dmail:<11}{wallet.mint_nft:<8}{wallet.votes:<10}')

                text += '\n'

            if edited:
                text += (f'\n--- Edited\№\t{"address":<72}{"name":<16}{"dmail":<10}{"shit_nft":<10}{"vote":<10}')
                for i, wallet in enumerate(imported):
                    text += (
                        f'\n{i + 1:<2}\t{wallet.address:<72}{wallet.name:<18}{wallet.dmail:<11}{wallet.mint_nft:<8}{wallet.votes:<10}')

                text += '\n'

            print(
                f'{text}\nDone! {config.LIGHTGREEN_EX}{len(imported)}/{total}{config.RESET_ALL} wallets were imported, '
                f'name have been changed at {config.LIGHTGREEN_EX}{len(edited)}/{total}{config.RESET_ALL}.'
            )

        else:
            print(f'{config.RED}There are no wallets on the file!{config.RESET_ALL}')
