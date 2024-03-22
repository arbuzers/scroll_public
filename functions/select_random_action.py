import random

from data.config import logger
from tasks.controller import Controller
from utils.db_api.models import Wallet
from functools import partial

from data.models import Settings
from libs.py_eth_async.data.models import Ether



def action_add(
        available_action,
        dmail=False,
        nft=False,
        voter=False
):
    weight = 0.2
    if dmail:
        action = available_action.send_dmail
    elif nft:
        action = available_action.mint_nft
        return [partial(action)], [weight]
    elif voter:
        action = available_action.vote
        return [partial(action)], [weight]
    else:
        logger.error("GLOBAL ERROR IN ADDING ACTION")
    return [partial(action)], [weight]


def check_eth_balance(eth_balance, settings, swap=True):
    if swap:
        return float(eth_balance.Ether) > float(settings.minimal_balance) * 1.5 + settings.eth_amount_for_swap.to_
    return float(eth_balance.Ether) > float(settings.minimal_balance)


async def select_random_action(controller: Controller, wallet: Wallet, initial: bool = True):
    settings = Settings()

    possible_actions = []
    weights = []

    dmail = 0
    nft = 0
    votes = 0

    eth_balance = await controller.client.wallet.balance()
    minimal_balance = Ether(settings.minimal_balance)
    if float(eth_balance.Ether) < float(minimal_balance.Ether):
        return 'Insufficient balance'

    if initial:
        tx_total, nft, dmail, votes = await controller.get_activity_count(wallet=wallet)
        msg = (f'{wallet.address} | total tx/action tx: {tx_total}/{nft + dmail + votes}'
               f' | amount NFT {nft}/{wallet.mint_nft}'
               f' | amount dmail {dmail}/{wallet.dmail}'
               f' | amount votes {votes}/{wallet.votes}')
        logger.info(msg)

        if dmail >= wallet.dmail and nft >= wallet.mint_nft and votes >= wallet.votes:
            return 'Processed'

    eth_balance = await controller.client.wallet.balance()

    # I - DMAIL
    if dmail < int(wallet.dmail):
        sufficient_balance = check_eth_balance(eth_balance, settings, swap=False)
        # Send email
        if sufficient_balance:
            actions, w = action_add(controller.dmail, dmail=True)
            possible_actions.extend(actions)
            weights.extend(w)
        else:
            msg = (f'{wallet.address} | Insufficient balance. Not possible to send email. Reason: actual '
                   f'ETH balance ({eth_balance.Ether}) must be more ({float(minimal_balance.Ether)}).')
            logger.warning(msg)

    # II VOTE
    if votes < int(wallet.votes):
        sufficient_balance = check_eth_balance(eth_balance, settings, swap=False)
        if sufficient_balance:
            actions, w = action_add(controller.voter, voter=True)
            possible_actions.extend(actions)
            weights.extend(w)
        else:
            msg = (f'{wallet.address} | Insufficient balance. Not possible vote action. Reason: actual '
                   f'ETH balance ({eth_balance.Ether}) must be more ({float(minimal_balance.Ether)}).')
            logger.warning(msg)

    # III - NFT
    if nft < int(wallet.mint_nft):
        sufficient_balance = check_eth_balance(eth_balance, settings, swap=False)
        if sufficient_balance:
            actions, w = action_add(controller.shitnft, nft=True)
            possible_actions.extend(actions)
            weights.extend(w)
        else:
            msg = (f'{wallet.address} | Insufficient balance. Not possible to mint nft. Reason: actual ETH balance'
                   f' ({eth_balance.Ether}) must be more ({float(minimal_balance.Ether)}).')
            logger.warning(msg)

    logger.info(f'Possible actions {len(possible_actions)} : {possible_actions}')
    if possible_actions:
        action = random.choices(possible_actions, weights=weights)[0]
        if action:
            return action

    msg = f'{wallet.address} | select_random_action | can not choose the action'
    logger.warning(msg)

    return None
