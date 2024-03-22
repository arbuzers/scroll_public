import random
from typing import Optional

import aiohttp
import requests
from aiohttp_socks import ProxyConnector
from eth_account.signers.local import LocalAccount
from fake_useragent import UserAgent
from web3 import Web3

from libs.py_eth_async.contracts import Contracts
from libs.py_eth_async.data.models import Network, Networks
from libs.py_eth_async.exceptions import InvalidProxy
from libs.py_eth_async.nfts import NFTs
from libs.py_eth_async.transactions import Transactions
from libs.py_eth_async.wallet import Wallet

from web3.eth import AsyncEth


class Client:
    """
    The client that is used to interact with all library functions.

    Attributes:
        network (Network): a network instance.
        account (Optional[LocalAccount]): imported account.
        w3 (Web3): a Web3 instance.

    """
    network: Network
    account: Optional[LocalAccount]
    w3: Web3

    def __init__(
            self, private_key: Optional[str] = None, network: Network = Networks.Goerli, proxy: Optional[str] = None,
            check_proxy: bool = True
    ) -> None:

        """
        Initialize the class.

        Args:
            private_key (str): a private key of a wallet, specify '' in order not to import the wallet.
                (generate a new one)
            network (Network): a network instance. (Goerli)
            proxy (Optional[str]): an HTTP or SOCKS5 IPv4 proxy in one of the following formats:

                - login:password@proxy:port
                - http://login:password@proxy:port
                - socks5://login:password@proxy:port
                - proxy:port
                - http://proxy:port

            check_proxy (bool): check if the proxy is working. (True)

        """
        self.network = network
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': UserAgent().chrome
        }
        self.proxy = proxy
        self.connector = None

        self.w3 = Web3(
            provider=Web3.AsyncHTTPProvider(
                endpoint_uri=self.network.rpc,
                request_kwargs={'proxy': self.proxy, 'headers': self.headers}
            ),
            modules={'eth': (AsyncEth,)},
            middlewares=[]
        )
        if private_key:
            self.account = self.w3.eth.account.from_key(private_key=private_key)

        elif private_key is None:
            self.account = self.w3.eth.account.create(extra_entropy=str(random.randint(1, 999_999_999)))

        else:
            self.account = None

        self.contracts = Contracts(self)
        self.nfts = NFTs(self)
        self.transactions = Transactions(self)
        self.wallet = Wallet(self)


    async def setup_proxy(self) -> Web3:
        provider = Web3.AsyncHTTPProvider(
            endpoint_uri=self.network.rpc, request_kwargs={'headers': self.headers}
        )
        await provider.cache_async_session(
            session=aiohttp.ClientSession(connector=self.connector, raise_for_status=True)
        )
        self.w3 = Web3(provider=provider)
        return self.w3
