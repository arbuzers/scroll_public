from curl_cffi.requests import AsyncSession

from fake_useragent import UserAgent
from typing import Optional

from libs.py_eth_async.client import Client
from aiohttp_proxy import ProxyConnector
from libs.py_eth_async.data.models import TxArgs, Ether, Wei, Unit, TokenAmount

from data.exceptions import GetOKlinkTokenBalanceError, NoApiKeyFound

from data.models import (
    Settings,
    Tokens,
)


OKLINK_URL = 'https://www.oklink.com'
CHAIN_SHORT_NAME = 'scroll'


class Base:
    def __init__(self, client: Client):
        self.client = client

    @staticmethod
    async def _get_txs(account_address: str, page: int = 1, limit: int = 50, proxy: Optional[str] = None) -> list[dict]:
        settings = Settings()

        if not proxy.startswith('http://'):
            proxy = f'http://{proxy}'

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': UserAgent().chrome,
            'Ok-Access-Key': settings.oklink_api_key,
        }

        params = {
            'chainShortName': CHAIN_SHORT_NAME,
            'address': account_address,
            'limit': limit,
            'page': page
        }
        async with AsyncSession() as session:
            response = await session.get('https://www.oklink.com/api/v5/explorer/address/transaction-list',
                                         params=params,
                                         headers=headers,
                                         proxy=proxy)
            response_json = response.json()
            return response_json['data'][0]['transactionLists']

    @staticmethod
    async def get_txs(account_address: str, proxy: Optional[str] = None) -> list[dict]:
        page = 1
        limit = 50
        txs_lst = []
        txs = await Base._get_txs(account_address=account_address, page=page, limit=limit, proxy=proxy)
        txs_lst += txs
        while len(txs) == limit:
            page += 1
            txs = await Base._get_txs(account_address=account_address, page=page, limit=limit, proxy=proxy)
            txs_lst += txs
        return txs_lst

    async def find_txs(
            self,
            to: str,
            function_name: str,
            txs: Optional[list[dict]] = None,
    ) -> list:

        if not txs:
            txs = await Base.get_txs(account_address=self.client.account.address, proxy=self.client.proxy)
        result_txs = []
        for tx in txs:
            if (
                    tx and
                    'state' in tx and
                    tx['state'] == 'success' and
                    'to' in tx and tx['to'].lower() == to.lower() and
                    'methodId' in tx and tx['methodId'].lower() == function_name.lower()
            ):
                result_txs.append(tx)
        return result_txs
