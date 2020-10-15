"""
parses location information received into python object
similar to kotlin's data classes
"""
# standard lib imports
from dataclasses import dataclass


@dataclass
class Location:
    title: str
    location_type: str
    latt_long: str
    woeid: int
