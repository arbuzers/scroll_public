import random
import inspect

from dataclasses import dataclass
from typing import Union, Optional

from libs.pretty_utils.miscellaneous.files import read_json
from libs.py_eth_async.data.models import Network, GWei, RawContract
from libs.pretty_utils.type_functions.classes import AutoRepr, Singleton, ArbitraryAttributes
from data.config import ABIS_DIR
from libs.py_eth_async.data.models import DefaultABIs
from data.config import SETTINGS_FILE


class ProgramActions:
    ImportWallets = ArbitraryAttributes(Selection=1)
    ExportWallets = ArbitraryAttributes(Selection=2)
    StartScript = ArbitraryAttributes(Selection=3)


@dataclass
class FromTo:
    from_: Union[int, float]
    to_: Union[int, float]


class BaseContract(RawContract):
    def __init__(self,
                 title,
                 address,
                 abi,
                 min_value: Optional[float] = 0,
                 stable: Optional[bool] = False,
                 belongs_to: Optional[str] = "",
                 decimals: Optional[int] = 18,
                 token_out_name: Optional[str] = '',
                 ):
        super().__init__(address, abi)
        self.title = title
        self.min_value = min_value
        self.stable = stable
        self.belongs_to = belongs_to
        self.decimals = decimals
        self.token_out_name = token_out_name


class WorkStatuses:
    Activity = 'activity'


class Settings(Singleton, AutoRepr):
    def __init__(self):
        json = read_json(path=SETTINGS_FILE)

        self.use_private_key_encryption = json['use_private_key_encryption']
        self.maximum_gas_price: GWei = GWei(json['maximum_gas_price'])
        self.oklink_api_key = json['oklink_api_key']

        self.rpcs = json['networks']['Scroll']['rpcs']

        self.minimal_balance: float = json['minimal_balance']
        self.activity_actions_delay: FromTo = FromTo(
            from_=json['activity_actions_delay']['from'], to_=json['activity_actions_delay']['to']
        )

        self.dmail: FromTo = FromTo(from_=json['dmail']['from'], to_=json['dmail']['to'])
        self.votes: FromTo = FromTo(from_=json['votes']['from'], to_=json['votes']['to'])
        self.mint_nft: FromTo = FromTo(from_=json['mint_nft']['from'],
                                       to_=json['mint_nft']['to'])


settings = Settings()

Scroll = Network(
    name='Scroll',
    rpc=random.choice(settings.rpcs),
    chain_id=534352,
    tx_type=0,
    coin_symbol='ETH',
    explorer='https://scrollscan.com/',
)


class Routers(Singleton):
    """
    An instance with router contracts
        variables:
            ROUTER: BaseContract
            ROUTER.title = any
    """

    DMAIL = BaseContract(
        title='dmail', address='0x47fbe95e981c0df9737b6971b451fb15fdc989d9',
        abi=read_json(path=(ABIS_DIR, 'dmail.json'))
    )

    RUBYSCORE = BaseContract(
        title="RUBY SCORE", address='0xe10Add2ad591A7AC3CA46788a06290De017b9fB4',
        abi=read_json(path=(ABIS_DIR, 'rubyscore.json'))
    )


class Tokens(Singleton):
    """
    An instance with token contracts
        variables:
            TOKEN: BaseContract
            TOKEN.title = symbol from OKLINK
    """
    ETH = BaseContract(
        title='ETH', address='0x0000000000000000000000000000000000000000',
        abi=DefaultABIs.Token,
        token_out_name="ETH",
    )

    ETH_E = BaseContract(
        title="ETH", address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
        abi=DefaultABIs.Token
    )

    WETH = BaseContract(
        title='WETH', address='0x5300000000000000000000000000000000000004',
        abi=read_json(path=(ABIS_DIR, 'WETH.json')),
        token_out_name="WETH",

    )

    @staticmethod
    def get_token_list():
        return [
            value for name, value in inspect.getmembers(Tokens)
            if isinstance(value, BaseContract)
        ]
