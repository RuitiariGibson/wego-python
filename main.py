from config.settings import Settings
from repo.backend.repository import initialize_method
from repo.frontend.frontend_repo import show_weather_information

"""
You can run the app via this main entry point or use the cli way instead
Either way the app will run """
if __name__ == '__main__':
    settings = Settings()
    initialize_method()
    print('Working please wait.... (^_*)')
    show_weather_information()
