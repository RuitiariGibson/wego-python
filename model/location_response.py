"""
parses location information received into python object
similar to kotlin's data classes
"""
from dataclasses import dataclass


@dataclass
class Location:
    title: str
    location_type: str
    latt_long: tuple
    woeid: int
