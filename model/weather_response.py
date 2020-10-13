from datetime import datetime
"""
Holds the weather response data
Essentially the class properties are updated via the setters
and accessed via getters hence supporting encapsulation principle
"""
from dataclasses import dataclass


@dataclass
class Weather:
    location: str
    weather_state_abbr: str
    created: str
    weather_state: str
    temp: float
    min_temp: float
    max_temp: float
    predictability: int
    humidity: int
    pressure: int
    applicability_date: datetime
