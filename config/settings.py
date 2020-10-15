from pathlib import Path
import configparser
from functools import lru_cache
import sys
"""
settings class which contains functions needed to persist the constants needed
 by the app
"""


class Settings:
    app_path =f'{Path.home()}/.wego'
    base_url = 'https://www.metaweather.com'
    config_file_path = f'{app_path}/appConfig.ini'
    config = configparser.ConfigParser()
    # this throws errno 13 error so strig literals to combine the files os.path.join(app_path, '/ appConfig.ini')

    def create_app_folder(self) -> bool:
        returnValue = False
        path = Path(self.app_path)
        try:
            path.mkdir(mode=0o777, exist_ok=True)
            returnValue = True
        except PermissionError as e:
            print(e)
            returnValue = False
        return returnValue
    """
    writes config file to the system
    """

    def write_config_file(self):
        self.config['URLS'] = {}
        self.config['URLS']['BASE_URL'] = self.base_url
        self.config['URLS']['WEATHER_URL'] = f'{self.base_url}/api/location'
        self.config['URLS']['LOCATION_URL'] = f'{self.base_url}/api/location/search/'
        self.config['LOCATION'] = {}
        self.config['LOCATION']['BASE_LOCATION'] = 'Nairobi'
        self.config['LOCATION']['BASE_LATT_LONG'] = '-1.270200, 36.804138'
        self.config['APPSTORAGE'] = {}
        self.config['APPSTORAGE']['BASE_APP_FOLDER'] = str(self.app_path)
        path = Path(self.app_path)
        if path.exists():
            self.__save()
        else:
            created = self.create_app_folder()
            if created:
                self.write_config_file()
            else:
                print('An error occurred please try again later')
                sys.exit()
    """
    This function returns the config values given a key only when needed
    then stores it in a cached state
    This ensures the reading process is faster rather than
    reading the whole values stored in the file at once
    params: key = of the value needed
    """
    @lru_cache(maxsize=None)
    def read_config_file(self, *, key: str, section: str) -> str:
        returnValue = None
        try:
            self.config.read(self.config_file_path)
            returnValue = self.config.get(section, key, fallback=None)
        except FileNotFoundError as e:
            print('No key associated with the section given')
            returnValue = ''
        return returnValue

    def config_exists(self) -> bool:
        path = Path(self.config_file_path)
        return path.exists()

    def update_location_name(self, location=None, latt_long=None):
        exists = self.config_exists()
        self.config.read(self.config_file_path)
        if exists:
            try:
                if location:
                    self.config.set('LOCATION', 'BASE_LOCATION', location)
                    self.__save()
                elif latt_long:
                    self.config.set('LOCATION', 'BASE_LATT_LONG', latt_long)
                    self.__save()
            except IOError as e:
                print('Failed to update the config file')

    def __save(self):
        with open(self.config_file_path, 'w') as file:
            self.config.write(file)
