import re
from functools import wraps
import requests
import time
import sys
"""
Method which checks whether the latt/long values are valid
example of a valid latt-long: 40.748,-73.985
"""


def latt_long_matcher(latt_long: str) -> bool:
    pattern = re.compile(r'^-?(.\d)*(\d+)?,-?(.\d)*(\d+)?$')
    return True if pattern.match(latt_long) else False


"""
Method which checks the internet connection
"""


def internet_checker(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            response = requests.head('https://www.google.com/', timeout=10)
            return f(*args, **kwargs)
        except requests.ConnectionError :
            no_connection = """

            \033[38;5;250m     \\-. \033[0m
            \033[38;5;250m  .-( \\ ).\033[0m
            \033[38;5;250m (__.__\\___)\033[0m
                 \033[38;5;21;1m   \\    \033[0m
            """
            print(no_connection)
            print('[*] This is embarassing...please check your internet connection and try again')
    return wrapper


"""
Ascii progress bar
"""


def progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function

    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100
                                                         * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
