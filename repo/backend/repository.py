# local imports
from config.settings import Settings
from utils.utils import latt_long_matcher
from exceptions.exceptions import InvalidLatt_LongValues
from utils.utils import internet_checker
from model.location_response import Location
from model.weather_response import Weather
# standard lib imports
import concurrent.futures
import requests
import time
from typing import List
import os
"""load location information """


# https://www.metaweather.com/api/location/search/?query=nairobi
# /api/location/search/?query=(query) /api/location/search/?lattlong=(latt),(long)
@internet_checker
def __load_location_response(url, timeout, *, location_name=None, latt_long=None):
    query_params = None
    if location_name:
        query_params = {'query': location_name}
    elif latt_long:
        query_params = {'lattlong': latt_long}
    with requests.get(url, params=query_params, timeout=timeout) as req:
        if req.status_code == 200:
            return req.json()
        else:
            print(req.reason)


@internet_checker
def __load_weather_response(url, *, woeid=None):
    if woeid:
        final_url = f'{url}/{woeid}'
        with requests.get(final_url, timeout=60) as response:
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print(
                    'The url is incorrect please check if the url corresponds to:https://meatweather.com/api/location/woeid')
            else:
                print(response.reason)


def parse_location_response():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        base_url = __return_location_base_url()
        future_to_url = None
        if base_url:
            location = __read_location_name()
            if location:
                future_to_url = executor.submit(
                    __load_location_response, base_url, 60, location_name=location.lower())
            else:
                latt_long = __read_latt_long_values()
                if latt_long:
                    future_to_url = executor.submit(
                        __load_location_response, base_url, 60, latt_long=latt_long)
            try:
                data = future_to_url.result()
                locationModel = None
                if data:
                    locationModel = Location(
                        data[0]['title'], data[0]['location_type'], data[0]['latt_long'], data[0]['woeid'])
                    return locationModel
            except Exception as exc:
                print('The following exception occurred: ', exc)


def parse_weather_information():
    locationModel = parse_location_response()
    # weatherResponseModel = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executors:
        weather_url = __return_weather_base_url()
        if weather_url:
            if locationModel:
                future = executors.submit(
                    __load_weather_response, weather_url, woeid=locationModel.woeid)
                try:
                    rawJson = future.result()
                    weatherArray = rawJson['consolidated_weather']
                    weather_objects = __return_weather_objects(
                        weatherArray, start_index=0, end_index=len(weatherArray)-1)
                    if len(weather_objects) > 1:
                        return weather_objects
                    # return weather_objects
                except Exception as exc:
                    print('The following exception occurred:', exc)
            else:
                return None
        else:
            print('Weather url is not set please set the url in the .config files')


def __return_location_base_url() -> str:
    returnValue = ''
    settings = Settings()
    exists = __config_exists()
    if exists:
        base_url = settings.read_config_file(
            key='LOCATION_URL', section='URLS')
        returnValue = base_url
    else:
        settings.write_config_file()
        __return_location_base_url()
    return returnValue


def __return_weather_base_url() -> str:
    returnValue = ''
    settings = Settings()
    weather_url = settings.read_config_file(key='WEATHER_URL', section='URLS')
    returnValue = weather_url
    return returnValue


def __read_location_name():
    settings = Settings()
    location = settings.read_config_file(
        key='BASE_LOCATION', section='LOCATION')
    if location:
        return location
    else:
        return 'nairobi'  # default


def __read_latt_long_values() -> str:
    settings = Settings()
    latt_long = settings.read_config_file(key='BASE_LATT_LONG',
                                          section='LOCATION')
    if latt_long:
        valid_latt_long = latt_long_matcher(latt_long)
        if valid_latt_long:
            return latt_long
        else:
            raise InvalidLatt_LongValues(
                'The latt-long values provided are invalid')


def __config_exists() -> bool:
    settings = Settings()
    return True if settings.config_exists() else False


def __read_config_values():
    settings = Settings()
    base_url = settings.read_config_file(
            key='LOCATION_URL', section='URLS')
    print(base_url)


def __return_weather_objects(weather_array: List[Weather],  start_index, end_index):
    weather_objects = []
    if end_index >= start_index:
        weather = Weather(**weather_array[start_index])
        weather_objects.append(weather)
        weather_objects += __return_weather_objects(
            weather_array, start_index+1, end_index)
    return weather_objects


def initialize_method():
    settings = Settings()
    config_exists = __config_exists()
    if not config_exists or os.path.getsize(settings.config_file_path) == 0:
        print('Configuring please wait...')
        settings.write_config_file()
        time.sleep(0.5)
        print('All done ^_^')
