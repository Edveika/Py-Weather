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

    def update_weather(self):
        # Wait for the user to choose a city
        while self.city == None: pass

        # Update the weather data every 30 minutes
        while not self.exit:
            api_response = self.api_manager.retrieve_api_data(self.city)

            if api_response == "NO_INTERNET_CONNECTION":
                while api_response == "NO_INTERNET_CONNECTION":
                    api_response = self.api_manager.retrieve_api_data(self.city)
                    time.sleep(30)
            elif api_response == "E400":
                while api_response == "E400":
                    api_response = self.api_manager.retrieve_api_data(self.city)
                    time.sleep(30)
            elif api_response == "CITY_NOT_FOUND": 
                self.city = None
                while self.city == None: pass
            elif api_response == "COORDINATE_RETRIEVE_FAILED":
                while api_response == "E400":
                    api_response = self.api_manager.retrieve_api_data(self.city)
                    time.sleep(30)

            time.sleep(1800)

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
    
    def get_weather_api(self):
        return self.api_manager