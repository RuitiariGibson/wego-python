# local imports
from repo.frontend.frontend_repo import show_weather_information
from repo.backend.repository import initialize_method


if __name__ == '__main__':
    initialize_method()
    print('Working please wait.... (^_*)')
    show_weather_information()
