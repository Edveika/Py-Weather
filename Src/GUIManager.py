import gi
# If multiple versions of GTK installed, make sure 3.0 is installed as well
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
from WeatherAPI import WeatherAPI, Status
from WeatherManager import WeatherManager
import threading
import time

class GUIManager:
    # Stores reference to weather manager inside self
    # Loads GUI .glade file
    # Asks user to input a city
    def __init__(self, weather_manager):
        # Reference to weather and api managers
        self.weather_manager = weather_manager
        self.api_manager = weather_manager.get_weather_api()

        # Create GtkBuilder instance and load .glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("GUI/Py-Weather-GUI.glade")

        # Ask user to input a city
        self.city_input_window()

        # If the city is not set and data is not received, wait because we cant display anything
        while not self.weather_manager.city_is_set() or not self.weather_manager.data_received():
            time.sleep(1)

        self.update_elements()

    # City input window
    # Simply gets input from the user, checks if city was found
    def city_input_window(self):
        input_window = self.builder.get_object("city_input_window")
        input_window.show_all()

        input_window.connect("destroy", Gtk.main_quit)

        input_box = self.builder.get_object("city_name_input")

        weather_manager = self.weather_manager
        def set_city_from_input(self):
            selected_city = str(Gtk.Entry.get_text(input_box))
            set_city_status = weather_manager.set_city(selected_city)
            if set_city_status == Status.SUCCESS:
                input_window.destroy()
                Gtk.main_quit()
                
        apply_city_btn = self.builder.get_object("apply_city")
        apply_city_btn.connect("clicked", set_city_from_input)

        Gtk.main()

    # The main window of the application
    # Shows weather data that was retrieved from open-meteo API of the city that the user chose
    def main_window(self):
        # Create new window
        window = self.builder.get_object("main_window")
        window.show_all()
        window.connect("destroy", Gtk.main_quit)

        # Refresh button pulls new data from the API and updates the GUI
        self.builder.get_object("weather_refresh").connect("clicked", self.manual_data_refresh)

        # Load the icons
        self.load_cur_data_icon()
        self.load_hourly_icons()

        Gtk.main()

    # When refresh button is pressed, new data gets pulled from the API
    def manual_data_refresh(self, buttton):
        if not self.update_thread.is_alive():
            self.update_thread.start()
        
    # Updates the GUI data of current weather
    def current_data_refresh(self):
        units = self.api_manager.get_current_units()

        city_temp = self.weather_manager.get_city() + ", " + str(round(self.api_manager.get_cur_temperature())) + units["temperature_2m"]
        self.builder.get_object("current_temperature").set_text(city_temp)

        cur_windspeed = str(self.api_manager.get_cur_windspeed()) + units["windspeed_10m"]
        self.builder.get_object("current_windspeed").set_text(cur_windspeed)

        cur_cloudcover = str(self.api_manager.get_cur_cloudcover()) + units["cloudcover"]
        self.builder.get_object("current_cloudcover").set_text(cur_cloudcover)

        cur_rain = str(self.api_manager.get_cur_rain()) + units["rain"]
        self.builder.get_object("current_rain").set_text(cur_rain)

        cur_snow = str(self.api_manager.get_cur_snowfall()) + units["snowfall"]
        self.builder.get_object("current_snow").set_text(cur_snow)

    # Updates the GUI data of hourly weather forecast
    def hourly_data_refresh(self):
        units = self.api_manager.get_hourly_units()

        for index in range(24):
            time = str(self.api_manager.get_hourly_time()[index])
            self.builder.get_object("hourly_time" + str(index)).set_text(time.split("T")[1])

            temperature = str(self.api_manager.get_hourly_temperature()[index]) + units["temperature_2m"]
            self.builder.get_object("hourly_temp" + str(index)).set_text("Temp: " + temperature)

            rain = str(self.api_manager.get_hourly_rain()[index]) + units["rain"]
            self.builder.get_object("hourly_rain" + str(index)).set_text("Rain: " + rain)
            
            snow = str(self.api_manager.get_hourly_snowfall()[index]) + units["snowfall"]
            self.builder.get_object("hourly_snow" + str(index)).set_text("Snow: " + snow)

            cloudcover = str(self.api_manager.get_hourly_cloudcover()[index]) + units["cloudcover"]
            self.builder.get_object("hourly_cloudcover" + str(index)).set_text("Cloudcover: " + cloudcover)

            windspeed = str(self.api_manager.get_hourly_windspeed()[index]) + units["windspeed_10m"]
            self.builder.get_object("hourly_windspeed" + str(index)).set_text("Wind: " + windspeed)

            precipitation_prob = str(self.api_manager.get_hourly_precipitation_probability()[index]) + units["precipitation_probability"]
            self.builder.get_object("hourly_rain_prob" + str(index)).set_text("Precip prob: " + precipitation_prob)
            
    # Updates the GUI data of daily weather forecast
    def daily_data_refresh(self):
        units = self.api_manager.get_daily_units()

        for index in range(7):
            windspeed = str(self.api_manager.get_daily_windspeed_max()[index]) + units["windspeed_10m_max"]
            self.builder.get_object("windspeed_daily" + str(index)).set_text("Wind: " + windspeed)
            
            precipitation_prob = str(self.api_manager.get_daily_precipitation_probability_max()[index]) + units["precipitation_probability_max"]
            self.builder.get_object("rain_prob_daily" + str(index)).set_text("Precip prob: " + precipitation_prob)

            precipitation_sum = str(self.api_manager.get_daily_precipitation_sum()[index]) + units["precipitation_sum"]
            self.builder.get_object("precipitation_sum_daily" + str(index)).set_text("Precip sum: " + precipitation_sum)

            sunset = str(self.api_manager.get_daily_sunset()[index])
            self.builder.get_object("sunset_daily" + str(index)).set_text("Sunset: " + sunset.split("T")[1])

            sunrise = str(self.api_manager.get_daily_sunrise()[index])
            self.builder.get_object("sunrise_daily" + str(index)).set_text("Sunrise: " + sunrise.split("T")[1])

            temp_max = str(self.api_manager.get_daily_temperature_max()[index]) + units["temperature_2m_max"]
            self.builder.get_object("temp_max_daily" + str(index)).set_text("Max temp: " + temp_max)

            temp_min = str(self.api_manager.get_daily_temperature_min()[index]) + units["temperature_2m_min"]
            self.builder.get_object("temp_min_daily" + str(index)).set_text("Min temp: " + temp_min)

            date = str(self.api_manager.get_daily_time()[index])
            self.builder.get_object("daily_date_daily" + str(index)).set_text(date)

    # Updates all GUI elements
    def update_elements(self):
        self.current_data_refresh()
        self.hourly_data_refresh()
        self.daily_data_refresh()

    # Loads image into GtkImage object and resizes it
    def load_icon(self, image, image_file, width, height):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_file)

        # Resize the image
        pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

        # Set the resized image as the source of the GtkImage widget
        image.set_from_pixbuf(pixbuf)

    # Determines which icon to use based on the weather conditions
    def set_data_icon(self, image, data):
        rain = data["rain"]
        snow = data["snowfall"]
        cloudcover = data["cloudcover"]

        if rain > 1:
            self.load_icon(image, "Assets/Icons/cloud_rain.png", 30, 30)
        elif snow > 1:
            self.load_icon(image, "Assets/Icons/cloud_snow.png", 30, 30)
        elif cloudcover >= 30:
            self.load_icon(image, "Assets/Icons/cloud.png", 30, 30)
        else:
            self.load_icon(image, "Assets/Icons/sunny.png", 30, 30)

    # Loads icon for current weather data
    def load_cur_data_icon(self):
        current_temperature = self.builder.get_object("current_weather_icon")
        self.set_data_icon(current_temperature, self.api_manager.get_cur_data())

        current_wind = self.builder.get_object("current_windspeed_icon")
        self.load_icon(current_wind, "Assets/Icons/wind.png", 30, 30)

        current_cloud = self.builder.get_object("current_cloudcover_icon")
        self.load_icon(current_cloud, "Assets/Icons/cloud.png", 30, 30)

        current_rain = self.builder.get_object("current_rain_icon")
        self.load_icon(current_rain, "Assets/Icons/rain.png", 30, 30)

        current_snow = self.builder.get_object("current_snow_icon")
        self.load_icon(current_snow, "Assets/Icons/snow.png", 30, 30)

    # Loads icons for hourly forecast
    def load_hourly_icons(self):
        for hour in range(24):
            weather_data = self.api_manager.get_hourly_data()
            data = {
                "rain": weather_data["rain"][hour],
                "snowfall": weather_data["snowfall"][hour],
                "cloudcover": weather_data["cloudcover"][hour]
            }
            icon = self.builder.get_object("icon_hourly" + str(hour))
            self.set_data_icon(icon, data)