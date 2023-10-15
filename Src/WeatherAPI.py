import requests
import json
from datetime import datetime

class WeatherAPI:
    def __init__(self):
        pass

    def connected_to_internet(self) -> bool:
        try:
            response = requests.get("http://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def retrieve_coordinates(self, city) -> str:
        if not self.connected_to_internet():
            return "NO_INTERNET_CONNECTION"
        
        api_response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}")
        if api_response.status_code == 200:
            location_data = json.loads(api_response.text)
            if len(location_data) == 1:
                return "CITY_NOT_FOUND"

            self.latitude = location_data["results"][0]["latitude"]
            self.longitude = location_data["results"][0]["longitude"]
            return "SUCCESS"
        elif api_response.status_code == 400:
            return "FAIL"

    def retrieve_api_data(self, city) -> str:
        if not self.connected_to_internet():
            return "NO_INTERNET_CONNECTION"
        
        coord_retrieve_status = self.retrieve_coordinates(city)
        if coord_retrieve_status == "FAIL" or coord_retrieve_status == "CITY_NOT_FOUND":
            return "COORDINATE_RETRIEVE_FAILED"

        api_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&current=temperature_2m,is_day,precipitation,rain,showers,snowfall,cloudcover,windspeed_10m,winddirection_10m&hourly=temperature_2m,precipitation_probability,rain,showers,snowfall,cloudcover,windspeed_10m,winddirection_10m,is_day&daily=temperature_2m_max,temperature_2m_min,sunrise,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,winddirection_10m_dominant&timezone=auto")
        
        if api_response.status_code == 200:
            self.weather_data = json.loads(api_response.text)
            return "SUCCESS"
        elif api_response.status_code == 400:
            return "FAIL"
    
    # Returns current temperature
    def get_cur_temperature(self) -> float:
        return self.weather_data["current"]["temperature_2m"]
    
    # Returns hourly temperature for 7 days from now
    def get_hourly_temperature(self) -> float:
        return self.weather_data["hourly"]["temperature_2m"]
    
    # Gets rain amount in mm
    def get_cur_rain(self) -> float:
        return self.weather_data["current"]["rain"]
    
    # Gets hourly rain for 7 days from now
    def get_hourly_rain(self) -> float:
        return self.weather_data["hourly"]["rain"]
    
    # Gets chance of precipitation for 7 days from now
    def get_hourly_precipitation_probability(self) -> int:
        return self.weather_data["hourly"]["precipitation_probability"]