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

        api_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&hourly=temperature_2m,rain,precipitation_probability")
        
        if api_response.status_code == 200:
            self.weather_data = json.loads(api_response.text)
            return "SUCCESS"
        elif api_response.status_code == 400:
            return "FAIL"
        
    def get_cur_temperature(self) -> float:
        hour = datetime.now().hour
        return self.weather_data["hourly"]["temperature_2m"][hour]
    
    def get_temperature(self, hour) -> float:
        return self.weather_data["hourly"]["temperature_2m"][hour]
    
    def get_cur_rain(self) -> float:
        hour = datetime.now().hour
        return self.weather_data["hourly"]["rain"][hour]
    
    def get_rain(self, hour) -> float:
        return self.weather_data["hourly"]["rain"][hour]
    
    def get_cur_precipitation_probability(self) -> int:
        hour = datetime.now().hour
        return self.weather_data["hourly"]["precipitation_probability"][hour]
    
    def get_precipitation_probability(self, hour) -> int:
        return self.weather_data["hourly"]["precipitation_probability"][hour]