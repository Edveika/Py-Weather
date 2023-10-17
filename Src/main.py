from WeatherAPI import WeatherAPI
from WeatherManager import WeatherManager
import threading

def main():
    # Creation of weather manager obj
    weather_manager = WeatherManager()

    # Weather Manager thread that is responsable for updating weather information
    wm_thread = threading.Thread(target=weather_manager.update_weather)
    wm_thread.start()

    # GUI will run here


main()