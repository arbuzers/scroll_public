from typing import Union, Dict, Any, Optional


def aiohttp_params(params: Optional[Dict[str, Any]]) -> Optional[Dict[str, Union[str, int, float]]]:
    """
    Convert requests params to aiohttp params.

    :param Optional[Dict[str, Any]] params: requests params
    :return Optional[Dict[str, Union[str, int, float]]]: aiohttp params
    """
    new_params = params.copy()
    if not params:
        return

    for key, value in params.items():
        if value is None:
            del new_params[key]

        if isinstance(value, bool):
            new_params[key] = str(value).lower()

        elif isinstance(value, bytes):
            new_params[key] = value.decode('utf-8')

    return new_params
