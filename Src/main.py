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

    # Creation of GUI manager object
    gui_manager = GUIManager(weather_manager)
    gui_manager.main_window()

    # Set exit flag to stop weather manager when main window is closed, exit the app
    weather_manager.set_exit_flag()

main()