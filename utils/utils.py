# standard lib imports
import re
from functools import wraps
import requests
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
