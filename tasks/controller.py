from typing import Optional
from libs.py_eth_async.client import Client

from data.models import Routers
from utils.db_api.models import Wallet

from tasks.base import Base
from tasks.dmail import Dmail
from tasks.shit_nfts import ShitNFTs
from tasks.rubyscore import RubyScore


class Controller(Base):
    def __init__(self, client: Client):
        super().__init__(client)

        self.base = Base(client=client)
        self.shitnft = ShitNFTs(client=client)
        self.dmail = Dmail(client=client)
        self.voter = RubyScore(client=client)

    async def get_activity_count(self, wallet: Wallet = None):
        # TODO get all activity
        txs = await Base.get_txs(account_address=self.client.account.address, proxy=wallet.proxy)
        tx_total = len(txs)
        dmail = await self.count_dmail(txs)
        nft = await self.count_nft(txs)
        votes = await self.count_votes(txs)
        return tx_total, nft, dmail, votes

    async def count_dmail(self, txs: Optional[list[dict]] = None, wallet: Wallet = None):
        result_count = 0

        if not txs:
            txs = await Base.get_txs(account_address=self.client.account.address, proxy=wallet.proxy)

        result_count += len(await self.find_txs(
            to=Routers.DMAIL.address,
            function_name='0x5b7d7482',
            txs=txs
        ))

        return result_count

    async def count_nft(self, txs: Optional[list[dict]] = None, wallet: Wallet = None):
        result_count = 0

        if not txs:
            txs = await Base.get_txs(account_address=self.client.account.address, proxy=wallet.proxy)

        for nft_name, nft_info in ShitNFTs.CONTRACT_MAP_NFT_PAY.items():
            contract_address = nft_info['contract_address']
            result_count += len(await self.find_txs(
                to=contract_address,
                function_name='0x1249c58b',
                txs=txs
            ))

        return result_count

    async def count_votes(self, txs: Optional[list[dict]] = None, wallet: Wallet = None):
        result_count = 0

        if not txs:
            txs = await Base.get_txs(account_address=self.client.account.address, proxy=wallet.proxy)

        result_count += len(await self.find_txs(
            to=Routers.RUBYSCORE.address,
            function_name='0x632a9a52',
            txs=txs
        ))

        return result_count
