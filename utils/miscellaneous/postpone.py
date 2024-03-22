import time
import random
from typing import Optional, List, Union

from data.models import Settings, WorkStatuses
from utils.db_api.database import db
from utils.db_api.models import Wallet


async def postpone(seconds: Optional[int] = 0, status: Optional[Union[str, List]] = WorkStatuses.Activity):
    settings = Settings()
    if isinstance(status, list):
        wallets = []
        for state in status:
            wallets_state: List[Wallet] = db.all(Wallet, Wallet.status.is_(state))
            wallets += wallets_state
            old_time = int(time.time())   
    else:
        wallets: List[Wallet] = db.all(Wallet, Wallet.status.is_(status))
    
    for wallet in wallets:
        now = int(time.time())    
        if isinstance(status, list):
            if wallet.next_pre_initial_action_time <= now:
                old_time = int(old_time) + random.randint(
                    int(settings.okx.delay_between_withdrawals.from_), 
                    int(settings.okx.delay_between_withdrawals.to_),
                )
                wallet.next_pre_initial_action_time = old_time

        elif status == WorkStatuses.Activity:
            if wallet.next_activity_action_time <= now:
                wallet.next_activity_action_time = now + random.randint(
                    0, int(settings.activity_actions_delay.to_ / 10)
                )

            elif seconds:
                wallet.next_activity_action_time = wallet.next_activity_action_time + seconds

        else:
            if wallet.next_initial_action_time <= now:
                wallet.next_initial_action_time = now + random.randint(0, int(settings.initial_actions_delay.to_ / 2))

            elif seconds:
                wallet.next_initial_action_time = wallet.next_initial_action_time + seconds

    db.commit()
