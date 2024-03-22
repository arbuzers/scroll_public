import math
import random
from decimal import Decimal
from typing import Optional, Union


def randfloat(from_: Union[int, float, str], to_: Union[int, float, str],
              step: Optional[Union[int, float, str]] = None) -> float:
    """
    Return a random float from the range.

    :param Union[int, float, str] from_: the minimum value
    :param Union[int, float, str] to_: the maximum value
    :param Optional[Union[int, float, str]] step: the step size (calculated based on the number of decimal places)
    :return float: the random float
    """
    from_ = Decimal(str(from_))
    to_ = Decimal(str(to_))
    if not step:
        step = 1 / 10 ** (min(from_.as_tuple().exponent, to_.as_tuple().exponent) * -1)

    step = Decimal(str(step))
    rand_int = Decimal(str(random.randint(0, int((to_ - from_) / step))))
    return float(rand_int * step + from_)


def float_range(from_: Union[int, float, str], to_: Union[int, float, str],
                step: Optional[Union[int, float, str]] = None) -> list:
    """
    Return a float range.

    :param Union[int, float, str] from_: a range start value
    :param Union[int, float, str] to_: the range stop value, not included
    :param Optional[Union[int, float, str]] step: a step size (calculated based on the number of decimal places)
    :return list: the range list
    """
    from_ = Decimal(str(from_))
    to_ = Decimal(str(to_))
    if not step:
        step = 1 / 10 ** (min(from_.as_tuple().exponent, to_.as_tuple().exponent) * -1)

    step = Decimal(str(step))
    range_list = []

    if from_ < to_:
        while from_ < to_:
            range_list.append(float(from_))
            from_ += step

    else:
        while from_ > to_:
            range_list.append(float(from_))
            from_ += step

    return range_list


def round_down(n: float, decimals: int = 0) -> float:
    """
    Round down a float number.

    :param float n: the float number
    :param int decimals: the decimals
    :return float: rounded down the float number
    """
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def round_up(n: float, decimals: int = 0) -> float:
    """
    Round up a float number.

    :param float n: the float number
    :param int decimals: the decimals
    :return float: rounded up the float number
    """
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
