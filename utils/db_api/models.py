from typing import Optional

from sqlalchemy.orm import declarative_base
from libs.pretty_utils.type_functions.classes import AutoRepr
from sqlalchemy import (Column, Integer, Text, Boolean)
from data.models import WorkStatuses

# --- Wallets
Base = declarative_base()


class Wallet(Base, AutoRepr):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    private_key = Column(Text, unique=True)
    address = Column(Text)
    name = Column(Text)
    proxy = Column(Text)
    mint_nft = Column(Integer)
    dmail = Column(Integer)
    votes = Column(Integer)
    next_activity_action_time = Column(Integer)
    status = Column(Text)
    completed = Column(Boolean)

    def __init__(self, private_key: str, proxy: str, dmail: int, mint_nft: int, votes: int,
                 address: Optional[str] = None, name: Optional[str] = None) -> None:
        self.private_key = private_key
        self.address = address
        self.name = name
        self.proxy = proxy
        self.dmail = dmail
        self.mint_nft = mint_nft
        self.votes = votes
        self.next_activity_action_time = 0
        self.status = WorkStatuses.Activity
        self.completed = False
