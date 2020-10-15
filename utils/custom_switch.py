"""
Python does note have a switch like syntax hence we can
use context manager (inform of a class) to replicate a switch- case statement
"""
from model.weather_status import WeatherType


class CustomSwitch:
    def __init__(self, value):
        self._val = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return False
    """
    Meat of the class since the value is stored
    we get the condition needed to be fullfiled in order
    to retrieve the value
    if the condition is satisfied we give out the stored value
    """

    def __call__(self, cond, *args):
        return self._val in (cond, )+args


def weather_status_switch(value):
    cloudy = """
         .--.
      .-(    ).
     (__.__)___)
    """

    hail = """
      .-.
     (   ).
    (___(__)
    o || || o
   ʻoʻ‚ʻoʻ‚ʻoʻ
    """

    light_rain = """
      .-.
     (   ).
    (___(__)
    ʻ ʻ ʻ ʻ
     ʻ ʻ ʻ ʻ
    """
    light_showers = """
        _`/\"\".-.
        ,\\_ (   ).
         /\(___(__)
          '⚡ʻʻʻʻ⚡ʻʻʻ
          ⚡ʻʻʻʻ⚡ʻʻʻ """
    light_sleet = """
       .-.
      (   ).
     (___(__)
     ʻ * ʻ *
      * ʻ * ʻ
    """

    light_snow = """
      .-.
     (   ).
    (___(__)
    ** ** *
    ** *** *
    """

    partly_cloud = """
       \\  /
     _ /\"\".-.
       \\_(   ).
       /\(___(__)
    """
    thunder_heavy_rain = """
      .-.
     (   ).
    (___(__)
    ‚ʻ⚡ʻ‚⚡ʻ
    ‚ʻ‚ʻ⚡ʻ‚ʻ
    """
    sunny = """
        \\   /
         .-.
      ‒ (   ) ‒
         `-᾿
        /   \\
    """
    thunderstorm = """
     ⚡  ⚡  ⚡
     * ⚡* ⚡*
     ⚡  ⚡  ⚡
     ⚡  ⚡  ⚡
    """
    with CustomSwitch(value) as status:
        if status(WeatherType.thunderstorm):
            return thunderstorm
        if status(WeatherType.heavyRain):
            return thunder_heavy_rain
        if status(WeatherType.showers):
            return light_showers
        if status(WeatherType.lightCloud):
            return partly_cloud
        if status(WeatherType.lightRain):
            return light_rain
        if status(WeatherType.sleet):
            return light_sleet
        if status(WeatherType.clear):
            return sunny
        if status(WeatherType.hail):
            return hail
        if status(WeatherType.snow):
            return light_snow
        else:
            return cloudy
