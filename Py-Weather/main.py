from WeatherManager import WeatherManager
from GUIManager import GUIManager
import threading

def main():
    # Creation of weather manager obj
    weather_manager = WeatherManager()

    # Weather Manager thread that is responsable for updating weather information
    wm_thread = threading.Thread(target=weather_manager.update_weather)
    wm_thread.start()

    try:
        # Creation of GUI manager object
        gui_manager = GUIManager(weather_manager)
    except SystemExit:
        # If exit was called from constructor, stop wm and exit
        weather_manager.set_exit_flag()
        wm_thread.join()
    # If the city was not set(user closed app or something)
    if not weather_manager.city_is_set():
        # Cleanup and close the program
        weather_manager.set_exit_flag()
        wm_thread.join()
        exit()
    else:
        # Starts the GUI
        try:
            gui_manager.main_window()
        except SystemExit:
            print("holly fuck")

    # Set exit flag to stop weather and GUI manager when main window is closed, exit the app
    weather_manager.set_exit_flag()
    gui_manager.set_exit_flag()

main()