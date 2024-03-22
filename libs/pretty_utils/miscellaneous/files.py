import json
import os
import sys
from typing import Optional, Union


def join_path(path: Union[str, tuple, list]) -> str:
    """
    Join the path passed in the list or tuple.

    :param Union[str, tuple, list] path: path to the object
    :return str: the joined path
    """
    if isinstance(path, str):
        return path

    return os.path.join(*path)


def touch(path: Union[str, tuple, list], file: bool = False) -> bool:
    """
    Create an object (file or directory) if it doesn't exist.

    :param Union[str, tuple, list] path: path to the object
    :param bool file: is it a file?
    :return bool: True if the object was created
    """
    path = join_path(path)
    if file:
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write('')

            return True

        return False

    if not os.path.isdir(path):
        os.mkdir(path)
        return True

    return False


def write_json(path: Union[str, tuple, list], obj: Union[list, dict], indent: Optional[int] = None,
               encoding: Optional[str] = None) -> None:
    """
    Write Python list or dictionary to a JSON file.

    :param Union[str, tuple, list] path: path to the JSON file
    :param Union[list, dict] obj: the Python list or dictionary
    :param Optional[int] indent: the indent level
    :param Optional[str] encoding: the name of the encoding used to decode or encode the file
    """
    path = join_path(path)
    with open(path, mode='w', encoding=encoding) as f:
        json.dump(obj, f, indent=indent)


def read_lines(path: Union[str, tuple, list], skip_empty_rows: bool = False, encoding: Optional[str] = None) -> list:
    """
    Read a file and return a list of lines.

    :param Union[str, tuple, list] path: path to the file
    :param bool skip_empty_rows: if True it doesn't include empty rows to the list
    :param Optional[str] encoding: the name of the encoding used to decode or encode the file
    :return list: the list of lines
    """
    path = join_path(path)
    with open(path, encoding=encoding) as f:
        lines = f.readlines()

    lines = [line.rstrip() for line in lines]
    if skip_empty_rows:
        lines = list(filter(lambda a: a, lines))

    return lines


def read_json(path: Union[str, tuple, list], encoding: Optional[str] = None) -> Union[list, dict]:
    """
    Read a JSON file and return a Python list or dictionary.

    :param Union[str, tuple, list] path: path to the JSON file
    :param Optional[str] encoding: the name of the encoding used to decode or encode the file
    :return Union[list, dict]: the Python list or dictionary
    """
    path = join_path(path)
    return json.load(open(path, encoding=encoding))


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    :param str relative_path: a relative path to the resource
    :return str: an absolute path to the resource
    """
    try:
        base_path = sys._MEIPASS

    except:
        base_path = os.path.abspath('')

    return os.path.join(base_path, relative_path)
