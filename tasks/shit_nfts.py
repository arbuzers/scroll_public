import random
from libs.py_eth_async.data.models import TokenAmount
from tasks.base import Base
from data.config import logger
from web3 import Web3


# Made by Toby
class ShitNFTs(Base):
    NAME = "Shit NFT"
    CONTRACT_MAP_NFT_PAY = {
        'PetrPIG': {
            'contract_address': '0x7994480d3c28aa75a8bf765ff42f7a555fd1ddf6',
            'mint_price': 0.00001267,
        },
        'Fuji': {
            'contract_address': '0x10bEB02B3e1EdC409396fc61446eBD482944258B',
            'mint_price': 0.00005,
        },
        'RobotHead': {
            'contract_address': '0x9fB411866b5f3fE09275E6Bf56C934d1Fa7AAE69',
            'mint_price': 0.00014,
        },
        'GoogleDollorBond': {
            'contract_address': '0x0D9c1fB69cc776FE109eA23A7Ae9068B56877E60',
            'mint_price': 0.000015,
        },
        'Pepe Dead': {
            'contract_address': '0x0001B42123484ac0e63110370634518d1C1dE5Bb',
            'mint_price': 0.000111,
        },
        'Robot is Painting': {
            'contract_address': '0xc16C89d2a18ad86DBa5E053903d49F07322e651D',
            'mint_price': 0.00007,
        },
        'Monro': {
            'contract_address': '0x4C653A42Dc26fD15DdBBb66ff76549A84a6129A9',
            'mint_price': 0.00020,
        },
        'NFT2Mi': {
            'contract_address': '0x9eb76EA6B31DB1ee5e5b4407DCE5832cB201CD50',
            'mint_price': 0.00003333,
        },
        'IDK': {
            'contract_address': '0xa588a3B49cA3d5e1EACab630222a901B828c0870',
            'mint_price': 0.00005,
        },
        'PORSCHE 928': {
            'contract_address': '0x378FEdaA39874fa3Bc08e01df08D12345Dce90c5',
            'mint_price': 0.00009280,
        },
        'Cadillac InnerSpace': {
            'contract_address': '0xc8C1663168c8A134f0165cCBaF9D7072Df21F637',
            'mint_price': 0.0000222,
        },
        'Mercedes-Maybach Vision 6 Cabriolet': {
            'contract_address': '0x039c2Af2bc9DD1AF5Cf18F01B52BE775df7eA7e1',
            'mint_price': 0.00006,
        },
        'The Elder Scrolls': {
            'contract_address': '0x5326f500C41c51E8Cd4f3c6451E142f05b23E85f',
            'mint_price': 0.000099,
        },
        'Jeep Wrangler Trailcat': {
            'contract_address': '0xB7a3453fACb2Da98180FF07E0Ac974a4B1FEF997',
            'mint_price': 0.00005,
        },
        'RobotGuash': {
            'contract_address': '0x6A91955b3b22D1eC31aD015FCf0e777427eB5CA6',
            'mint_price': 0.0001,
        },
    }

    async def mint_nft(self):
        failed_text = f'Failed mint NFT chip NFT'

        random_nft_name = random.choice(list(ShitNFTs.CONTRACT_MAP_NFT_PAY.keys()))
        logger.info(f'Start mint Shit NFT | {random_nft_name}')

        value = TokenAmount(amount=ShitNFTs.CONTRACT_MAP_NFT_PAY[random_nft_name]['mint_price'])
        address = ShitNFTs.CONTRACT_MAP_NFT_PAY[random_nft_name]['contract_address']

        try:
            tx_params = {
                'gasPrice': (await self.client.transactions.gas_price(w3=self.client.w3)).Wei,
                'from': self.client.account.address,
                'to': Web3.to_checksum_address(address),
                'data': '0x1249c58b',
                'value': value.Wei
            }

            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
            if receipt:
                msg = f'{self.client.account.address} | Mint NFT "{random_nft_name}" successes! | {tx.hash.hex()}'
                return msg
            logger.warning(failed_text)
            return f'{self.client.account.address} | {failed_text}!'

        except BaseException as e:
            logger.exception(f'Mint {random_nft_name} | Contract: {address}')
            return f'{failed_text}: {e}'
