import multiprocessing
import os
import sys
import time
from typing import Union


def get_input(stdin_fd, queue, prompt):
    sys.stdin = os.fdopen(stdin_fd)
    try:
        text = input(prompt)
        queue.put(text)

    except:
        pass


def timeout_input(prompt: str, timeout: Union[int, float] = 60, default_value: str = '', end: str = '\n') -> str:
    """
    Ask a user to enter a string, and if he doesn't do so in a certain amount of time, return the default value.
    Works only in if __name__ == '__main__' construction.

    :param str prompt: a prompt that will be displayed before the input request
    :param Union[int, float] timeout: a timeout after which the default value will be returned (60)
    :param str default_value: a default value that will be returned after the timeout expires (empty string)
    :param str end: string appended after the last value (two newlines)
    :return str: the inputted or default value
    """
    text = default_value
    queue = multiprocessing.Queue()
    input_process = multiprocessing.Process(target=get_input, args=(sys.stdin.fileno(), queue, prompt))
    input_process.start()
    start = time.time()
    while time.time() - start < timeout:
        if not queue.empty():
            text = queue.get()
            break

        time.sleep(0.05)

    input_process.terminate()
    print(end, end='')
    return text
