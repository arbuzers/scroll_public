from typing import List, Optional

from libs.pretty_utils.databases import sqlalchemy_, sqlite

from data.config import WALLETS_DB
from utils.db_api.models import Wallet, Base


# --- Functions
def get_wallet(private_key: str, sqlite_query: bool = False) -> Optional[Wallet]:
    if sqlite_query:
        return sqlite.DB(WALLETS_DB).execute('SELECT * FROM wallets WHERE private_key = ?', (private_key,), True)

    return db.one(Wallet, Wallet.private_key == private_key)


def get_wallets(sqlite_query: bool = False) -> List[Wallet]:
    if sqlite_query:
        return sqlite.DB(WALLETS_DB).execute('SELECT * FROM wallets')

    return db.all(Wallet)


# --- Miscellaneous
db = sqlalchemy_.DB('sqlite:///files/wallets.db', pool_recycle=3600, connect_args={'check_same_thread': False})

db.create_tables(Base)
