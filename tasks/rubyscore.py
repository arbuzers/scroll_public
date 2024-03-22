from web3.types import TxParams

from data.models import Routers
from tasks.base import Base
from data.config import logger


class RubyScore(Base):
    NAME = 'RubyScore'

    async def vote(self):
        failed_text = f'Failed vote via {self.NAME}'
        contract = await self.client.contracts.get(contract_address=Routers.RUBYSCORE)

        try:
            tx_params = TxParams(
                to=contract.address,
                data=contract.encodeABI('vote'),
            )

            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
            if receipt:
                msg = f'{self.client.account.address} success vote via {self.NAME}'
                return msg

        except BaseException as e:
            logger.exception(f'RubyScore.vote | VOTE')
            return f'{self.client.account.address} {failed_text}: {e}'
