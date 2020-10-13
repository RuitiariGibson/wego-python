import re
"""
Method which checks whether the latt/long values are valid
example of a valid latt-long: 40.748,-73.985
"""


def latt_long_matcher(latt_long: str) -> bool:
    pattern = re.compile(r'^-?(.\d)*(\d+)?,-?(.\d)*(\d+)?$')
    return True if pattern.match(latt_long) else False
