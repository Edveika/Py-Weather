from WeatherAPI import WeatherAPI, Status
import threading
import time

class WeatherManager:
    def __init__(self) -> None:
        self.city = None
        self.exit = False
        self.api_manager = WeatherAPI()

    # Mainloop of this program
    # Updates weather data
    # Takes care of possible errors that the user may encounter
    def update_weather(self) -> None:
        # Program will run until exit flag is set
        while not self.exit:
            # If the user chose a city
            if self.city != None:
                # Get data from the API
                api_response = self.api_manager.retrieve_api_data(self.city)

                # If there is no internet connection, error 400 was returned on cordinate retrieve failed(error 400 returned in coordinate retrieve function)
                while api_response == Status.ERROR_NO_INTERNET or api_response == Status.ERROR_400:
                    # Just keep trying to reach the API data, there is not much else we can do
                    api_response = self.api_manager.retrieve_api_data(self.city)
                    time.sleep(30)

                print(self.api_manager.get_cur_temperature())
                # Update the weather data every 60 minutes
                time.sleep(3600)
            
            # So we dont waste too much resources
            time.sleep(1)

    # Sets location(where we want to see the forecast)
    # Also checks for any potential errors
    def set_city(self, city) -> str:
        # Get coordinates of the city from the API. If value is returned, it means the city does exist
        api_response = self.api_manager.retrieve_coordinates(city)

        # If something failed, return the error message
        if api_response != Status.SUCCESS:
            return api_response

        # If nothing failed and city is valid, set the city name
        self.city = city

        # Return success
        return Status.SUCCESS
    
    # Returns API manager that gets updated after x minutes and stores all needed data
    def get_weather_api(self) -> WeatherAPI:
        return self.api_manager
    
weather = WeatherManager()

weather.set_city("Kaunas")
weather.update_weather()