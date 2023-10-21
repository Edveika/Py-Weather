from WeatherAPI import WeatherAPI
from WeatherManager import WeatherManager
from GUIManager import GUIManager
import threading

def main():
    # Creation of weather manager obj
    weather_manager = WeatherManager()

    # Weather Manager thread that is responsable for updating weather information
    wm_thread = threading.Thread(target=weather_manager.update_weather)
    wm_thread.start()

    # Creation of GUI manager obj
    gui_manager = GUIManager(weather_manager)
    gui_manager.main_window()

    # set exit flag to stop weather manager when window closed
    weather_manager.set_exit_flag()

    # Wait for the weather manager to close and exit the program
    wm_thread.join()


main()