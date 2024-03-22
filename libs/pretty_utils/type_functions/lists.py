import math


def split_list(s_list: list, n: int = 100, parts: bool = False) -> list:
    """
    Split a list to several lists.

    :param list s_list: a list to split
    :param int n: split the list into parts of N elements (100)
    :param bool parts: split the list into N parts (False)
    :return list: the split list
    """
    if parts:
        n = math.ceil(len(s_list) / n)

    if len(s_list) > n:
        lists = []
        for i in range(0, len(s_list), n):
            lists.append(s_list[i:i + n])

    else:
        lists = [s_list]

    return lists


def replace_to_null(r_list: list) -> list:
    """
    Replace all None in a list with 0.

    :param list r_list: a list to replace
    :return list: the processed list
    """
    for i in range(len(r_list)):
        if r_list[i] is None:
            r_list[i] = 0

    return r_list
