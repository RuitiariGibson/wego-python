from datetime import datetime
"""
Holds the weather response data

"""
from dataclasses import dataclass


@dataclass
class Weather:
    id: int
    weather_state_abbr: str
    created: str
    weather_state_name: str
    the_temp: float
    min_temp: float
    max_temp: float
    predictability: int
    humidity: int
    air_pressure: int
    wind_direction: float
    wind_speed: float
    wind_direction_compass: float
    applicable_date: datetime
    visibility: float
