from config.settings import Settings
import urllib
import urllib.request
import concurrent.futures
from utils.utils import latt_long_matcher
from exceptions.exceptions import InvalidLatt_LongValues
"""load location information -1.270200,36.804138"""


def __load_location_response(url, timeout, *, location_name=None, latt_long=None):
    query_params = {'query': location_name}
    encoded_params = urllib.parse.urlencode(query_params).encode('utf-8')
    with urllib.request.urlopen(url, encoded_params, timeout) as conn:
        print(conn.code_)
        return conn.read()


def parse_location_response():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        base_url = __return_base_url()
        print(base_url)
        future_to_url = None
        if base_url:
            location = __read_location_name()
            if location:
                print(location.lower())
                future_to_url = executor.submit(
                    __load_location_response, base_url, 60, location_name=location.lower())
            else:
                latt_long = __read_latt_long_values()
                print(latt_long)
                if latt_long:
                    future_to_url = executor.submit(
                        __load_location_response, base_url, 60, location_name=latt_long)
            if future_to_url.done():
                try:
                    data = future_to_url.result()
                    print(data)
                except Exception as exc:
                    print('The following exception occurred: ', exc)


def __return_base_url() -> str:
    returnValue = ''
    settings = Settings()
    exists = __config_exists()
    if exists:
        base_url = settings.read_config_file(
            key='LOCATION_URL', section='URLS')
        returnValue = base_url
    else:
        settings.write_config_file()
        __return_base_url()
    return returnValue


def __read_location_name():
    settings = Settings()
    location = settings.read_config_file(
        key='BASE_LOCATION', section='LOCATION')
    if location:
        return location
    else:
        return None


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
    config_exists = settings.config_exists()
    if config_exists:
        base_url = settings.read_config_file(
            key='LOCATION_URL', section='URLS')
        print(base_url)
    else:
        settings.write_config_file()
        __read_config_values()
