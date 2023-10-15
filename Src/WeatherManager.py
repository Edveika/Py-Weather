from WeatherAPI import WeatherAPI
import threading

import time
import os

class WeatherManager:
    def __init__(self):
        # Will prompt the user to enter their city
        self.city = None
        self.exit = False
        self.api_manager = WeatherAPI()

    def set_city(self, city) -> str:
        # Get coordinates of the city from the api
        api_response = self.api_manager.retrieve_coordinates(city)

        # If user has no internet connection, return connection failed and promp the user via GUI to connect to the internet
        if api_response == "NO_INTERNET_CONNECTION":
            return "NO_INTERNET_CONNECTION"
        # If the user's city is not found, prompt the user via GUI to try again
        elif api_response == "CITY_NOT_FOUND":
            return "CITY_NOT_FOUND"
        # If error 400 was returned, prompt user via GUI to try later
        elif api_response == "FAIL":
            return "FAIL"

        self.city = city

        return "SUCCESS"