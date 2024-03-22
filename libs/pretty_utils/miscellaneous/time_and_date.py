import time
from datetime import datetime, timezone, timedelta
from typing import Optional, Union


def strtime_to_unix(strtime: str, utc_offset: int = 0, format: str = '%d.%m.%Y %H:%M') -> int:
    """
    Convert string time to unix.

    :param str strtime: a string time
    :param int utc_offset: hour offset from UTC (0)
    :param str format: format for string time parsing (%d.%m.%Y %H:%M)
    :return int: the unix time
    """
    return int(datetime.strptime(strtime, format).replace(
        tzinfo=timezone(timedelta(seconds=utc_offset * 60 * 60))).timestamp())


def unix_to_strtime(unix_time: Union[int, float, str] = None, utc_offset: Optional[int] = None,
                    format: str = '%d.%m.%Y %H:%M:%S') -> str:
    """
    Convert unix to string time. In particular return the current time.

    :param Union[int, float, str] unix_time: a unix time (current)
    :param int utc_offset: hour offset from UTC (None)
    :param str format: format for string time output (%d.%m.%Y %H:%M:%S)
    :return str: the string time
    """
    if not unix_time:
        unix_time = time.time()

    if isinstance(unix_time, str):
        unix_time = int(unix_time)

    if utc_offset is None:
        strtime = datetime.fromtimestamp(unix_time)
    elif utc_offset == 0:
        strtime = datetime.utcfromtimestamp(unix_time)
    else:
        strtime = datetime.utcfromtimestamp(unix_time).replace(tzinfo=timezone.utc).astimezone(
            tz=timezone(timedelta(seconds=utc_offset * 60 * 60)))

    return strtime.strftime(format)
