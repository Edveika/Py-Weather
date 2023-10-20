from WeatherAPI import WeatherAPI
from WeatherManager import WeatherManager
from gui import GUIManager
import threading

def main():
    # Creation of weather manager obj
    weather_manager = WeatherManager()

    weather_manager.set_city("Kaunas")

    # Weather Manager thread that is responsable for updating weather information
    wm_thread = threading.Thread(target=weather_manager.update_weather)
    wm_thread.start()

    # Creation of GUI manager obj
    gui_manager = GUIManager(weather_manager)


main()