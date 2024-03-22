import time
import random
import asyncio
from typing import List

from libs.py_eth_async.client import Client
from libs.pretty_utils.miscellaneous.time_and_date import unix_to_strtime
from data import config
from data.config import semaphore, lock, logger
from data.models import Settings, Scroll, WorkStatuses
from libs.py_eth_async.data.models import Networks
from utils.db_api.database import db
from utils.db_api.models import Wallet
from tasks.controller import Controller
from utils.encryption import get_private_key
from utils.miscellaneous.postpone import postpone
from utils.miscellaneous.print_summary import print_summary
from functions.select_random_action import select_random_action


async def update_expired() -> None:
    now = int(time.time())
    expired_wallets: List[Wallet] = db.all(
        Wallet, Wallet.status.is_(WorkStatuses.Activity) & (Wallet.next_activity_action_time <= now)
    )

    if expired_wallets:
        settings = Settings()
        for wallet in expired_wallets:
            wallet.next_activity_action_time = now + random.randint(0, int(settings.activity_actions_delay.to_ / 10))
            logger.info(f'Action time was re-generated: {unix_to_strtime(wallet.next_activity_action_time)}.')
        db.commit()


async def start_task(wallet):
    async with semaphore:
        settings = Settings()
        client = Client(
            private_key=get_private_key(wallet.private_key),
            network=Scroll,
            proxy=wallet.proxy
        )

        controller = Controller(client=client)
        action = await select_random_action(controller=controller, wallet=wallet, initial=True)
        now = int(time.time())
        if action == 'Insufficient balance':
            wallet.next_activity_action_time = now + random.randint(
                int(settings.activity_actions_delay.from_ / 10), int(settings.activity_actions_delay.to_ / 10)
            )
            logger.warning(f'Insufficient balance!')
        if action == 'Processed':
            wallet.next_activity_action_time = now + random.randint(
                int(settings.activity_actions_delay.from_ / 10), int(settings.activity_actions_delay.to_ / 10)
            )

            logger.success(f'{wallet.address} | Finished all tasks')

        elif action:
            status = await action()
            now = int(time.time())
            if 'Failed' not in status:
                wallet.next_activity_action_time = now + random.randint(
                    settings.activity_actions_delay.from_, settings.activity_actions_delay.to_
                )
                logger.success(status)

            else:
                wallet.next_activity_action_time = now + random.randint(5 * 60, 10 * 60)
                logger.error(status)
        async with lock:
            db.commit()


async def activity() -> None:
    delay = 10
    summary_print_time = 0
    next_message_time = 0
    await update_expired()
    try:
        next_action_time = min((wallet.next_activity_action_time for wallet in db.all(
            Wallet, Wallet.status.is_(WorkStatuses.Activity)
        )))
        logger.info(f'The next closest action will be performed at {unix_to_strtime(next_action_time)}.')
    except:
        logger.error('Unable to update next activity time')
        pass
    while True:
        try:
            now = int(time.time())

            if summary_print_time <= now:
                await print_summary()
                summary_print_time = now + 30 * 60

            wallets: Wallet = db.all(
                Wallet, Wallet.status.is_(WorkStatuses.Activity) & (Wallet.next_activity_action_time <= now)
            )

            if wallets:
                settings = Settings()
                client = Client(private_key='', network=Networks.Ethereum)
                gas_price = await client.transactions.gas_price(w3=client.w3)

                if float(gas_price.GWei) > settings.maximum_gas_price:
                    await postpone(seconds=int(delay / 2), status=WorkStatuses.Activity)
                    if next_message_time <= time.time():
                        next_message_time = now + 30 * 60
                        logger.info(f'Current gas price is too high: {gas_price.GWei} > {settings.maximum_gas_price.GWei}!')
                    continue

                task = []
                for wallet in wallets:
                    task.append(asyncio.create_task(start_task(wallet)))

                await asyncio.gather(*task)

                try:
                    next_action_time = min((wallet.next_activity_action_time for wallet in db.all(
                        Wallet, Wallet.status.is_(WorkStatuses.Activity)
                    )))
                    logger.info(f'The next closest action will be performed at {unix_to_strtime(next_action_time)}.')

                except:
                    logger.error('Unable to reshedule to wallet')
                    pass

        except BaseException as e:
            logger.error(f'Activity - Something went wrong: {e}')

        finally:
            await asyncio.sleep(delay)


color = config.GREEN
thread = 'Activity'
