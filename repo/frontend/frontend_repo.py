# local imports
from model.weather_status import WeatherType
from utils.custom_switch import weather_status_switch
from repo.backend.repository import parse_weather_information
# standard lib imports
import tabulate
import dateutil.parser
from datetime import datetime


def show_weather_information():
    weather_objects = parse_weather_information()
    # today and Tomorrow
    today = weather_objects[0]
    tomorrow = weather_objects[1]
    next_day_object = weather_objects[2]
    # icons
    today_icon = weather_status_switch(
        __return_weather_state_from_abbr(weather_objects[0].weather_state_abbr))
    tomorrows_icon = weather_status_switch(
        __return_weather_state_from_abbr(weather_objects[1].weather_state_abbr))
    next_day_icon = weather_status_switch(
        __return_weather_state_from_abbr(next_day_object.weather_state_abbr))
    # max and min temperatures
    min_temp_today = __format_temp(round(weather_objects[0].min_temp, 1))
    max_temp_today = __format_temp(round(weather_objects[0].max_temp, 1))
    min_temp_tomorrow = __format_temp(round(weather_objects[1].min_temp, 1))
    max_temp_tomorrow = __format_temp(round(weather_objects[1].max_temp, 1))
    next_day_max_temp = __format_temp(round(next_day_object.max_temp, 1))
    next_day_min_temp = __format_temp(round(next_day_object.min_temp, 1))
    # air pressure
    todays_pressure = __format_air_pressure(
        round(weather_objects[0].air_pressure))
    tomorrows_pressure = __format_air_pressure(
        round(weather_objects[1].air_pressure))
    next_day_pressure = __format_air_pressure(
        round(next_day_object.air_pressure))
    # speed of wind
    todays_speed_of_wind = __format_speed_of_wind(
        round(weather_objects[0].wind_speed, 1))
    tomorrows_speed = __format_speed_of_wind(
        round(weather_objects[1].wind_speed, 1))
    next_day_speed_of_wind = __format_speed_of_wind(
        round(next_day_object.wind_speed, 1))
    # humidity
    todays_humidity = __format_humidity(round(weather_objects[0].humidity, 1))
    tomorrows_humidity = __format_humidity(
        round(weather_objects[1].humidity, 1))
    next_day_humidity = __format_humidity(round(next_day_object.humidity, 1))
    next_day = _format_weather_date(weather_objects[2].applicable_date)
    table = [
     [f'{today.weather_state_name.ljust(10)} {today_icon}', f'{tomorrow.weather_state_name.ljust(10)} {tomorrows_icon}',
      f'{next_day_object.weather_state_name.ljust(10)} {next_day_icon}'],
     [f'{max_temp_today} ─ {min_temp_today}', f'{max_temp_tomorrow} ─ {min_temp_tomorrow}',
         f'{next_day_max_temp} ─ {next_day_min_temp}'],
     [f'{todays_pressure} ', f'{tomorrows_pressure}',  f'{next_day_pressure}'],
     [f'{todays_speed_of_wind} ', f'{tomorrows_speed}',
         f'{next_day_speed_of_wind}'],
     [f'{todays_humidity} ', f'{tomorrows_humidity}', f'{next_day_humidity}']
    ]
    print(tabulate.tabulate(table, tablefmt='grid', headers=[
                      'Today', 'Tomorrow', next_day]), end='')


def _format_weather_date(raw_date: str) -> str:
    dt = dateutil.parser.parse(raw_date)
    format = "%a %b %d"
    return datetime.strftime(dt, format)


def __return_weather_state_from_abbr(abbr: str):
    if abbr == 'sn':
        return WeatherType.snow
    elif abbr == 'sl':
        return WeatherType.sleet
    elif abbr == 'h':
        return WeatherType.hail
    elif abbr == 't':
        return WeatherType.thunderstorm
    elif abbr == 'hr':
        return WeatherType.heavyRain
    elif abbr == 'lr':
        return WeatherType.lightRain
    elif abbr == 's':
        return WeatherType.showers
    elif abbr == 'hc':
        return WeatherType.heavyCloud
    elif abbr == 'lc':
        return WeatherType.lightCloud
    elif abbr == 'c':
        return WeatherType.clear
    else:
        return WeatherType.unknown


# normal room temp = 20 Celcius
def __format_temp(temp):
    returnTemp = ''
    if temp == 20:
        returnTemp = "\033[32m"+str(temp)+"\033[0m"   # green normal
    elif temp < 20:
        returnTemp = '\033[38;5;111m' + str(temp) + '\033[0m'  # blue chilly
    else:
        returnTemp = '\033[31m'+str(temp)+'\033[0m '  # red sweltering hot
    return returnTemp + " °C"


# normal pressure is 1013.25 mbar
def __format_air_pressure(pressure):
    pressure_icons = ["↓ ",  "↑ "]
    finalPressure = ''
    if pressure == 1013:
        finalPressure = str(pressure)
    elif pressure < 1013:
        finalPressure = pressure_icons[0] + str(pressure)
    else:
        finalPressure = pressure_icons[1] + str(pressure)
    return finalPressure + " mbar"


"""
calm = 0-13 mph
moderate speed == 13-18mph
fresh breeze == 19-24 mph
strong breeze == 25 -31 mph
"""


def __format_speed_of_wind(speed):
    # represents a 360 degrees swipe from 0
    speed_icons = ["↙ ",  "↖ ", "↑ ", "↗ ", "↘ "]
    returnSpeed = ''
    if speed in range(0, 14):
        returnSpeed = speed_icons[0] + str(speed)
    elif speed in range(13, 19):
        returnSpeed = speed_icons[1] + str(speed)
    elif speed in range(19, 25):
        returnSpeed = speed_icons[2] + str(speed)
    elif speed in range(25, 32):
        returnSpeed = speed_icons[3] + str(speed)
    else:
        returnSpeed = speed_icons[4] + str(speed)
    return returnSpeed + " mph"


def __format_humidity(humidity):
    finalHumidity = '\033[38;5;111m' + 'ʻ' + str(humidity) + ' %' + '\033[0m'
    return finalHumidity
