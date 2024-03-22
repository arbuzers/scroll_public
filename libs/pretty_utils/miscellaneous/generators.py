from random import choice, randint
from string import ascii_lowercase, ascii_uppercase, digits


def nickname(len: int = 9, capital: bool = False) -> str:
    """
    Deprecated, use username.
    """
    return username(len, capital)


def username(len: int = 9, capital: bool = False) -> str:
    """
    Generate a username.

    :param len: length of a username (9)
    :param capital: capitalize the first letter (False)
    :return: the generated username
    """
    vowels = ('a', 'e', 'i', 'o', 'u', 'y')
    consonants = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z',
                  'sh', 'zh', 'ch', 'kh', 'th')

    is_vowels_first = bool(randint(0, 1))
    result = ''
    for i in range(0, len):
        is_even = i % 2 == 0
        if (is_vowels_first and is_even) or (not is_vowels_first and not is_even):
            result += choice(vowels)

        else:
            result += choice(consonants)

    if capital:
        return result.title()

    return result


def password(len: int = 16, use_capitals: bool = True, use_digits: bool = True, use_specials: bool = False) -> str:
    """
    Generate a password.

    :param len: length of a password (16)
    :param use_capitals: use capitals letters (True)
    :param use_digits: use digits (True)
    :param use_specials: use special symbols (False)
    :return: the generated password
    """
    lowers = ascii_lowercase
    capitals = ascii_uppercase
    specials = '+-/*!&$#?=@<>'
    chars = lowers
    if use_capitals:
        chars += capitals

    if use_digits:
        chars += digits

    if use_specials:
        chars += specials

    password = ''
    for i in range(len):
        password += choice(chars)

    exist = False
    for letter in lowers:
        if letter in password:
            exist = True
            break

    if not exist:
        password = password[1:] + choice(lowers)

    if use_capitals:
        exist = False
        for letter in capitals:
            if letter in password:
                exist = True
                break

        if not exist:
            password = password[1:] + choice(capitals)

    if use_digits:
        exist = False
        for letter in digits:
            if letter in password:
                exist = True
                break

        if not exist:
            password = password[1:] + choice(digits)

    if use_specials:
        exist = False
        for letter in specials:
            if letter in password:
                exist = True
                break

        if not exist:
            password = password[1:] + choice(specials)

    return password
