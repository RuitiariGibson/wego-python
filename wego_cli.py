# standard libs
import click
# local imports
from config.settings import Settings
from repo.backend.repository import initialize_method
from repo.frontend.frontend_repo import show_weather_information


@click.command()
@click.option('--location', type=str, help='Location name of the weather update you want')
def wego(location):
    settings = Settings()
    initialize_method()
    if location is not None:
        settings.update_location_name(location=location)
    print('Working please wait.... (^_*)')
    show_weather_information()
