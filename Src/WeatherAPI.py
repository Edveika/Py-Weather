import requests
import json
from enum import Enum

class Status(Enum):
    SUCCESS = 0
    ERROR_NO_INTERNET = 1
    ERROR_CITY_NOT_FOUND = 2
    ERROR_400 = 3

class WeatherAPI:
    def __init__(self):
        self.weather_data = None

    def connected_to_internet(self) -> bool:
        try:
            response = requests.get("http://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def retrieve_coordinates(self, city) -> str:
        api_response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}")
        
        if api_response.status_code == 200:
            location_data = json.loads(api_response.text)
            if len(location_data) == 1:
                return Status.ERROR_CITY_NOT_FOUND

            self.latitude = location_data["results"][0]["latitude"]
            self.longitude = location_data["results"][0]["longitude"]
            return Status.SUCCESS
        elif api_response.status_code == 400:
            return Status.ERROR_400

    def retrieve_api_data(self, city) -> str:
        if not self.connected_to_internet():
            return Status.ERROR_NO_INTERNET
        
        coord_retrieve_response = self.retrieve_coordinates(city)
        if coord_retrieve_response != Status.SUCCESS:
            return coord_retrieve_response
        
        api_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&current=temperature_2m,is_day,precipitation,rain,showers,snowfall,cloudcover,windspeed_10m,winddirection_10m&hourly=temperature_2m,precipitation_probability,rain,showers,snowfall,cloudcover,windspeed_10m,winddirection_10m,is_day&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,winddirection_10m_dominant&timezone=auto&windspeed_unit=ms")
        
        if api_response.status_code == 200:
            self.weather_data = json.loads(api_response.text)
            return Status.SUCCESS
        elif api_response.status_code == 400:
            return Status.ERROR_400
    
    ##
    ## Current time data
    ##

    # Returns current weather data
    def get_cur_data(self):
        return self.weather_data["current"]

    # Returns units of current weather data
    def get_current_units(self):
        return self.weather_data["current_units"]

    # Returns current temperature
    def get_cur_temperature(self) -> float:
        return self.weather_data["current"]["temperature_2m"]
    
    # Returns current rain amount in mm
    def get_cur_rain(self) -> float:
        return self.weather_data["current"]["rain"]

    # Returns preceding hour sum of showers(mm)
    def get_cur_showers(self) -> float:
        return self.weather_data["current"]["showers"]
    
    # Returns preceding hour sum of snow(cm)
    def get_cur_snowfall(self) -> float:
        return self.weather_data["current"]["snowfall"]

    # Returns current % of total cloud cover
    def get_cur_cloudcover(self) -> int:
        return self.weather_data["current"]["cloudcover"]
    
    # Returns current windspeed
    def get_cur_windspeed(self) -> float:
        return self.weather_data["current"]["windspeed_10m"]
    
    # Returns wind direction in degrees
    def get_cur_wind_dir(self) -> float:
        return self.weather_data["current"]["winddirection_10m"]

    # Returns 1 if day 0 if night
    def is_day(self) -> bool:
        return bool(self.weather_data["current"]["is_day"])

    # Returns precipitation
    def get_cur_precipitation(self):
        return self.weather_data["current"]["precipitation"]
    
    ##
    ## Hourly data 
    ##

    # Returns hourly data
    def get_hourly_data(self):
        return self.weather_data["hourly"]

    # Returns units of hourly weather data
    def get_hourly_units(self):
        return self.weather_data["hourly_units"]

    # Gets date and time for 7 days from now
    def get_hourly_time(self):
        return self.weather_data["hourly"]["time"]

    # Returns hourly temperature for 7 days from now
    def get_hourly_temperature(self) -> float:
        return self.weather_data["hourly"]["temperature_2m"]

    # Returns hourly rain list for 7 days from now
    def get_hourly_rain(self):
        return self.weather_data["hourly"]["rain"]
    
    # Returns hourly showers list for 7 days from now
    def get_hourly_showers(self):
        return self.weather_data["hourly"]["showers"]

    # Returns hourly snowfall list for 7 days from now
    def get_hourly_snowfall(self):
        return self.weather_data["hourly"]["snowfall"]

    # Returns hourly cloudcover list for 7 days from now
    def get_hourly_cloudcover(self):
        return self.weather_data["hourly"]["cloudcover"]
    
    # Returns hourly windspeed list for 7 days from now
    def get_hourly_windspeed(self):
        return self.weather_data["hourly"]["windspeed_10m"]
    
    # Returns hourly wind direction list for 7 days from now
    def get_hourly_wind_dir(self):
        return self.weather_data["hourly"]["winddirection_10m"]
    
    # Returns bool is day list for 7 days from now
    def get_hourly_is_day(self):
        return self.weather_data["hourly"]["is_day"]

    # Returns chance of precipitation in % list for 7 days from now
    def get_hourly_precipitation_probability(self):
        return self.weather_data["hourly"]["precipitation_probability"]
    
    ##
    ## Daily data
    ##

    # Returns daily weather data
    def get_daily_data(self):
        return self.weather_data["daily"]

    # Returns units of daily weather data
    def get_daily_units(self):
        return self.weather_data["daily_units"]

    # Returns a list of dates 7 days from now
    def get_daily_time(self):
        return self.weather_data["daily"]["time"]
    
    # Returns a list of minimum temperatures 7 days from now
    def get_daily_temperature_min(self):
        return self.weather_data["daily"]["temperature_2m_min"]
    
    # Returns a list of maximum temperatures 7 days from now
    def get_daily_temperature_max(self):
        return self.weather_data["daily"]["temperature_2m_max"]
    
    # Returns a list of daily sunrise time
    def get_daily_sunrise(self):
        return self.weather_data["daily"]["sunrise"]
    
    # Returns a list of daily sunset time
    def get_daily_sunset(self):
        return self.weather_data["daily"]["sunset"]
    
    # Returns a list of daily sunrise time
    def get_daily_precipitation_sum(self):
        return self.weather_data["daily"]["precipitation_sum"]
    
    # Returns list of daily rain sum(mm)
    def get_daily_rain_sum(self):
        return self.weather_data["daily"]["rain_sum"]
    
    # Returns list of daily showers sum(mm)
    def get_daily_showers_sum(self):
        return self.weather_data["daily"]["showers_sum"]
    
    # Returns list of daily snowfall sum(cm)
    def get_daily_snowfall_sum(self):
        return self.weather_data["daily"]["snowfall_sum"]
    
    # Returns list of daily sum of hours with rain
    def get_daily_precipitation_hours(self):
        return self.weather_data["daily"]["precipitation_hours"]
    
    # Returns list of daily maximum probability of precipitation
    def get_daily_precipitation_probability_max(self):
        return self.weather_data["daily"]["precipitation_probability_max"]
    
    # Returns list of daily maximum windspeed(m/s)
    def get_daily_windspeed_max(self):
        return self.weather_data["daily"]["windspeed_10m_max"]
    
    # Returns a list of daily dominant wind direction
    def get_daily_wind_dir(self):
        return self.weather_data["daily"]["winddirection_10m_dominant"]