import gi
# If multiple versions of GTK installed, make sure 3.0 is installed as well
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from WeatherManager import WeatherManager
import os

class GUIManager:
    def __init__(self, weather_manager):
        self.weather_manager = weather_manager
        self.api_manager = weather_manager.get_weather_api()

        builder = Gtk.Builder()
        builder.add_from_file("Py-Weather-GUI.glade")

        window = builder.get_object("main_window")
        window.show_all()

        self.temp_label = builder.get_object("current_temperature")
        self.windspeed_label = builder.get_object("current_windspeed")
        self.cloudcover_label = builder.get_object("current_cloudcover")
        self.rain_label = builder.get_object("current_rain")
        self.showers_label = builder.get_object("current_showers")
        self.snow_label = builder.get_object("current_snow")

        refresh_button = builder.get_object("weather_refresh")
        refresh_button.connect("clicked", self.refresh_weather_data)


        Gtk.main()

    def city_input_window(self):
        pass

    def main_window(self):
        pass

    # TODO: add units
    def refresh_weather_data(self, buttton):
        units = self.api_manager.get_current_units()

        self.temp_label.set_text("Current temperature: " + str(self.api_manager.get_cur_temperature()) + units["temperature_2m"])
        self.windspeed_label.set_text("Current wind speed: " + str(self.api_manager.get_cur_windspeed()) + units["cloudcover"])
        self.cloudcover_label.set_text("Current cloud cover: " + str(self.api_manager.get_cur_cloudcover()) + units["cloudcover"])
        self.rain_label.set_text("Current rain: " + str(self.api_manager.get_cur_rain()) + units["rain"])
        self.showers_label.set_text("Current showers: " + str(self.api_manager.get_cur_showers()) + units["showers"])
        self.snow_label.set_text("Current snow: " + str(self.api_manager.get_cur_snowfall()) + units["snowfall"])