from typing import Optional, Union


def text_between(text: str, begin: str = '', end: str = '') -> str:
    """
    Extract a text between strings.

    :param str text: a source text
    :param str begin: a string from the end of which to start the extraction
    :param str end: a string at the beginning of which the extraction should end
    :return str: the extracted text or empty string if nothing is found
    """
    try:
        if begin:
            start = text.index(begin) + len(begin)

        else:
            start = 0

    except:
        start = 0

    try:
        if end:
            end = text.index(end, start)

        else:
            end = len(text)

    except:
        end = len(text)

    excerpt = text[start:end]
    if excerpt == text:
        return ''

    return excerpt


def del_ws(text: str) -> str:
    """
    Delete whitespaces.

    :param str text: a source text
    :return str: the text without whitespaces
    """
    return text.replace(' ', '').replace('\t', '')


def format_number(number: Union[int, float], decimals: Optional[int] = None, thousands_separator: str = ' ') -> str:
    """
    Return formatted number like 3 392 233,9420.

    :param Union[int, float] number: a number for formatting
    :param Optional[int] decimals: how many decimal places to round a number
    :param str thousands_separator: thousands separator
    :return str: the formatted number
    """
    if decimals is not None:
        number = round(number, decimals)

    formatted_number = '{0:,}'.format(number)
    if thousands_separator == '.':
        formatted_number = formatted_number.replace(',', ' ').replace('.', ',').replace(' ', '.')

    else:
        formatted_number = formatted_number.replace(',', thousands_separator)
        if thousands_separator == ' ':
            formatted_number = formatted_number.replace('.', ',')

    return formatted_number
