from WeatherAPI import WeatherAPI, Status
import threading
import time

UPDATE_INTERVAL = 3600

class WeatherManager:
    def __init__(self) -> None:
        self.city = None
        self.exit = False
        self.api_manager = WeatherAPI()

    # Mainloop of this program
    # Updates weather data
    # Takes care of possible errors that the user may encounter
    def update_weather(self) -> None:
        self.last_update = time.time()
        # Initialized to UPDATE_INTERVAL so it updates on launch
        self.wait_time = UPDATE_INTERVAL

        # Program will run until exit flag is set
        while not self.exit:
            # If the user chose a city
            if self.city != None:
                # Updates every UPDATE_INTERVAL
                if self.wait_time >= UPDATE_INTERVAL:
                    # Get data from the API
                    api_response = self.get_new_weather_data()

                    # If there is no internet connection, error 400 was returned on cordinate retrieve failed(error 400 returned in coordinate retrieve function)
                    while api_response != 200:
                        # Just keep trying to reach the API data, there is not much else we can do
                        api_response = self.get_new_weather_data()
                        time.sleep(5)
                    
                    # Reset the start timer to current time
                    self.last_update = time.time()

                # Get current time
                cur_time = time.time()

                # Get wait time
                self.wait_time = cur_time - self.last_update

    # Gets new data from the API
    def get_new_weather_data(self):
        return self.api_manager.retrieve_api_data(self.city)

    # Returns the last time(date) that the weather info got updated
    def get_last_update(self):
        return self.last_update
    
    def set_last_update(self, date):
        self.last_update = date

    # Sets location(where we want to see the forecast)
    # Also checks for any potential errors
    def set_city(self, city) -> str:
        # Get coordinates of the city from the API. If value is returned, it means the city does exist
        api_response = self.api_manager.retrieve_coordinates(city)

        # If something failed, return the error message
        if api_response != 200:
            return api_response

        # If nothing failed and city is valid, set the city name
        self.city = city

        # Return api_message(that is 200)
        return api_response
    
    # Returns API manager that gets updated after x minutes and stores all needed data
    def get_weather_api(self) -> WeatherAPI:
        return self.api_manager
    
    # Returns city that is currently set
    def get_city(self) -> str:
        return self.city

    # When set the Weather Manager exits
    def set_exit_flag(self):
        self.exit = True

    # Checks if city is already set
    # True - set
    # False - None
    def city_is_set(self) -> bool:
        return False if self.city is None else True
    
    # Checks if data was received from the API
    def data_received(self) -> bool:
        return False if not self.get_weather_api().retrieved_data() else True