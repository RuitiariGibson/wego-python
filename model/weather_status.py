import enum
"""
Holds the weather status information eg snow, lr etc
"""


class WeatherType(enum.Enum):
    snow = 'snow'
    sleet = 'Sleet'
    hail = 'Hail'
    thunderstorm = 'Thunderstorm'
    heavyRain = 'Heavy Rain'
    lightRain = 'Light Rain'
    showers = 'Showers'
    heavyCloud = 'Heavy Cloud'
    clear = 'Clear'
    lightCloud = 'Light Cloud'
    unknown = 'unknown'
