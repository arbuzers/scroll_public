import hashlib
from faker import Faker
from loguru import logger

from web3.types import TxParams
from libs.py_eth_async.data.models import TxArgs

from tasks.base import Base
from data.models import Routers


class Dmail(Base):
    async def send_dmail(self):
        logger.info(f'Preparing Fake User (e-mail, theme)')
        failed_text = f'Failed send e-mail via Dmail'

        email_address, theme_info = await Dmail.fake_acc()
        to = await Dmail.sha256(email_address)
        theme = await Dmail.sha256(theme_info)

        contract = await self.client.contracts.get(contract_address=Routers.DMAIL)

        params = TxArgs(
            email=to,
            theme=theme,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('send_mail', args=params.tuple()),
        )

        logger.info(f'Sending e-mail to: {email_address} theme: {theme_info} - via Dmail')

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)

        if receipt:
            return f'E-mail was sent to {email_address} via Dmail: TX-Hash {tx.hash.hex()}'
        return f'{failed_text}!'

    @staticmethod
    async def fake_acc():
        fake = Faker()
        profile = fake.profile()
        email_address, theme = profile['mail'], fake.company()

        return email_address, theme

    @staticmethod
    async def sha256(data):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode('utf-8'))
        hash_str = sha256_hash.hexdigest()

        return hash_str
