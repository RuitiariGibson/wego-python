from pathlib import Path
import configparser
import os
from functools import lru_cache
import sys
"""
settings class which contains functions needed to persist the constants needed
 by the app
"""


class Settings:
    app_path =f'{Path.home()}/.wego'
    db_file_path = os.path.join(app_path, '/database')
    base_url = 'https://www.metaweather.com'
    config_file_path = f'{app_path}/appConfig.ini'
    # this throws errno 13 error so strig literals to combine the files os.path.join(app_path, '/ appConfig.ini')

    def create_app_folder(self) -> bool:
        returnValue = False
        msg = ''
        path = Path(self.app_path)
        try:
            path.mkdir(mode=0o777, exist_ok=True)
            returnValue = True
            msg = None
        except PermissionError as e:
            print(e)
            returnValue = False
        return returnValue
    """
    writes config file to the system
    essentially this method should be called on a background thread
    """

    def write_config_file(self):
        config = configparser.ConfigParser()
        config['URLS'] = {}
        config['URLS']['BASE_URL'] = self.base_url
        config['URLS']['WEATHER_URL'] = f'{self.base_url}/api/location'
        config['URLS']['LOCATION_URL'] = f'{self.base_url}/api/location/search/'
        config['LOCATION'] = {}
        config['LOCATION']['BASE_LOCATION'] = 'Nairobi'
        config['LOCATION']['BASE_LATT_LONG'] = '46.90,-90.0'
        config['APPSTORAGE'] = {}
        config['APPSTORAGE']['BASE_APP_FOLDER'] = str(self.app_path)
        config['APPSTORAGE']['DATABASE_FILE_PATH'] = self.db_file_path
        path = Path(self.app_path)
        if path.exists():
            with open(self.config_file_path, 'w') as configFile:
                config.write(configFile)
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
        config = configparser.ConfigParser()
        returnValue = None
        try:
            config.read(self.config_file_path)
            returnValue = config.get(section, key, fallback=None)
        except FileNotFoundError as e:
            sys.stderr(e)
            returnValue = ''
        return returnValue

    def config_exists(self) -> bool:
        path = Path(self.config_file_path)
        return path.exists()
