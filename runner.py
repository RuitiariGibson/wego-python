from repo.repository import parse_weather_information
from model.weather_response import Weather
from typing import List


def return_weather_objects(weather_array: List[Weather],  start_index, end_index):
    weather_objects = []
    if end_index >= start_index:
        weather = Weather(**weather_array[start_index])
        weather_objects.append(weather)
        weather_objects += return_weather_objects(weather_array, start_index+1, end_index)
    return weather_objects

if __name__ == "__main__":
    # https://www.metaweather.com/api/location/search/?query=nairobi
    # /api/location/search/?query=(query) /api/location/search/?lattlong=(latt),(long)
    #  /api/location/search/?query=(query) /api/location/search/?lattlong=(latt),(long)
    weather_response = parse_weather_information()
    print(weather_response)
    #    weather_two = Weather(**array)
    #    print(weather_two)
    # print(weather['consolidated_weather'])
    # results = [{'title': 'Nairobi', 'location_type': 'City', 'woeid': 1528488, 'latt_long': '-1.270200,36.804138'}]
