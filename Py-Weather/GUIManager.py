import gi
# If multiple versions of GTK installed, make sure 3.0 is installed as well
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
from WeatherAPI import WeatherAPI, APIStatus
from WeatherManager import WeatherManager
import threading
import time
import os

class GUIManager:
    # Stores reference to weather manager inside self
    # Loads GUI .glade file
    # Asks user to input a city
    def __init__(self, weather_manager: WeatherManager):
        # Exit flag for GUI element auto-update
        self.exit = False

        # Bool for manual refresh button
        self.manual_refresh = False

        # Reference to weather and api managers
        self.weather_manager = weather_manager
        self.api_manager: WeatherAPI = weather_manager.get_weather_api()
        
        # Get path to this file
        self.cur_path = os.path.dirname(os.path.abspath(__file__))

        # Create GtkBuilder instance and load .glade file
        self.builder = Gtk.Builder()

        # If .glade file does not exist
        if not os.path.exists(self.cur_path + "/GUI/Py-Weather-GUI.glade"):
            # Show an error and exit
            self.show_message_box(Gtk.MessageType.ERROR, "Not found: " + self.cur_path + "/GUI/Py-Weather-GUI.glade")
            exit()
        self.builder.add_from_file(self.cur_path + "/GUI/Py-Weather-GUI.glade")

        # Ask user to input a city and if the city is set, draw the gui
        if self.city_input_window():
            # If the city is not set or data is not received, wait because we cant display anything
            while not self.weather_manager.city_is_set() or not self.api_manager.retrieved_data():
                time.sleep(1)

            # Start auto-update thread
            refresh_thread = threading.Thread(target=self.data_refresh)
            refresh_thread.start()

            # Load the icons
            self.load_cur_image()
            self.load_hourly_image()

    # City input window
    # Simply gets input from the user, checks if city was found
    # Returns true if city was set, false if it was not set
    def city_input_window(self) -> bool:
        input_window = self.builder.get_object("city_input_window")
        input_window.show_all()
        input_window.connect("destroy", Gtk.main_quit)

        input_box = self.builder.get_object("city_name_input")
        current_self = self

        def set_city_from_input(button):
            nonlocal current_self
            selected_city = str(Gtk.Entry.get_text(input_box)).upper()
            set_city_status = current_self.weather_manager.set_city(selected_city)
            if set_city_status == APIStatus.SUCCESS.value:
                input_window.destroy()
                Gtk.main_quit()
            elif set_city_status == APIStatus.ERROR_NO_INTERNET:
                current_self.show_message_box(Gtk.MessageType.ERROR, "No internet connection")
            elif set_city_status == APIStatus.ERROR_CITY_NOT_FOUND:
                current_self.show_message_box(Gtk.MessageType.ERROR, "City not found")
            elif set_city_status != APIStatus.SUCCESS.value:
                current_self.show_message_box(Gtk.MessageType.ERROR, "ERROR: " + str(set_city_status))
                
        apply_city_btn = self.builder.get_object("apply_city")
        apply_city_btn.connect("clicked", set_city_from_input)

        Gtk.main()
        return True if self.weather_manager.get_city() else False

    # The main window of the application
    # Shows weather data that was retrieved from open-meteo API of the city that the user chose
    def main_window(self):
        # Create new window
        window = self.builder.get_object("main_window")
        window.show_all()
        window.connect("destroy", Gtk.main_quit)

        # Refresh button pulls new data from the API and updates the GUI
        self.builder.get_object("weather_refresh").connect("clicked", self.manual_data_refresh)

        Gtk.main()

    # Updates GUI elements once weather manager updates
    # Updates only GUI because weather manager updates the data every UPDATE_INTERVAL, so doing it here is not needed
    # Runs in a separate thread so it can update in the background
    def data_refresh(self):
        last_update = None

        # If exit flag is set, the loop will close, function will return
        while not self.exit:
             # Syncs with weather manager's update
            if last_update != self.weather_manager.get_last_update():
                api_response = self.weather_manager.get_response()

                if api_response == APIStatus.SUCCESS.value:
                    # Update the gui elements
                    self.update_elements()
                    # Set last update date of the data(not GUI)
                    last_update = self.weather_manager.get_last_update()
                elif api_response == APIStatus.ERROR_NO_INTERNET:
                    self.show_message_box(Gtk.MessageType.ERROR, "Data refresh fail, no internet connection")
                elif api_response != APIStatus.SUCCESS.value:
                    self.show_message_box(Gtk.MessageType.ERROR, "ERROR: " + str(api_response))
            # If refresh button was clicked
            if self.manual_refresh:
                # Checks if atleast 1 minute passed between the updates and if so updates the data once again
                if self.api_manager.can_refresh():
                    # Refresh data, update GUI
                    api_response = self.weather_manager.get_new_weather_data()
                    if api_response == APIStatus.SUCCESS.value:
                        self.update_elements()
                    elif api_response == APIStatus.ERROR_NO_INTERNET:
                        self.show_message_box(Gtk.MessageType.ERROR, "Data refresh fail, no internet connection")
                    elif api_response != APIStatus.SUCCESS.value:
                        self.show_message_box(Gtk.MessageType.ERROR, "ERROR: " + str(api_response))

                    # Reset manual update flag
                    self.manual_refresh = False
                # If 1 minute did not pass
                else:
                    # Refresh flag gets turned off
                    self.manual_refresh = False
                    # Error message box is shown
                    self.show_message_box(Gtk.MessageType.ERROR, "ERROR: " + "Wait atleast 60 seconds before refreshing")

    # When refresh button is pressed, manual update flag is set
    def manual_data_refresh(self, buttton):
        self.manual_refresh = True
        
    # Updates the GUI data of current weather
    def update_current_elements(self):
        units = self.api_manager.get_current_units()

        city_temp = self.weather_manager.get_city() + ", " + str(round(self.api_manager.get_cur_temperature())) + units["temperature_2m"]
        self.builder.get_object("current_temperature").set_text(city_temp)

    # Updates the GUI data of hourly weather forecast
    def update_hourly_elements(self):
        units = self.api_manager.get_hourly_units()

        for hour in range(24):
            time = str(self.api_manager.get_hourly_time()[hour])
            self.builder.get_object("hourly_time" + str(hour)).set_text(time.split("T")[1])

            temperature = str(self.api_manager.get_hourly_temperature()[hour]) + units["temperature_2m"]
            self.builder.get_object("hourly_temp" + str(hour)).set_text("Temp: " + temperature)

            rain = str(self.api_manager.get_hourly_rain()[hour]) + units["rain"]
            self.builder.get_object("hourly_rain" + str(hour)).set_text("Rain: " + rain)
            
            snow = str(self.api_manager.get_hourly_snowfall()[hour]) + units["snowfall"]
            self.builder.get_object("hourly_snow" + str(hour)).set_text("Snow: " + snow)

            cloudcover = str(self.api_manager.get_hourly_cloudcover()[hour]) + units["cloudcover"]
            self.builder.get_object("hourly_cloudcover" + str(hour)).set_text("Cloudcover: " + cloudcover)

            windspeed = str(self.api_manager.get_hourly_windspeed()[hour]) + units["windspeed_10m"]
            self.builder.get_object("hourly_windspeed" + str(hour)).set_text("Wind: " + windspeed)

            precipitation_prob = str(self.api_manager.get_hourly_precipitation_probability()[hour]) + units["precipitation_probability"]
            self.builder.get_object("hourly_rain_prob" + str(hour)).set_text("Precip prob: " + precipitation_prob)
            
    # Updates the GUI data of daily weather forecast
    def update_daily_elements(self):
        units = self.api_manager.get_daily_units()

        for day in range(7):
            windspeed = str(self.api_manager.get_daily_windspeed_max()[day]) + units["windspeed_10m_max"]
            self.builder.get_object("windspeed_daily" + str(day)).set_text("Wind: " + windspeed)
            
            precipitation_prob = str(self.api_manager.get_daily_precipitation_probability_max()[day]) + units["precipitation_probability_max"]
            self.builder.get_object("rain_prob_daily" + str(day)).set_text("Precip prob: " + precipitation_prob)

            precipitation_sum = str(self.api_manager.get_daily_precipitation_sum()[day]) + units["precipitation_sum"]
            self.builder.get_object("precipitation_sum_daily" + str(day)).set_text("Precip sum: " + precipitation_sum)

            sunset = str(self.api_manager.get_daily_sunset()[day])
            self.builder.get_object("sunset_daily" + str(day)).set_text("Sunset: " + sunset.split("T")[1])

            sunrise = str(self.api_manager.get_daily_sunrise()[day])
            self.builder.get_object("sunrise_daily" + str(day)).set_text("Sunrise: " + sunrise.split("T")[1])

            temp_max = str(self.api_manager.get_daily_temperature_max()[day]) + units["temperature_2m_max"]
            self.builder.get_object("temp_max_daily" + str(day)).set_text("Max temp: " + temp_max)

            temp_min = str(self.api_manager.get_daily_temperature_min()[day]) + units["temperature_2m_min"]
            self.builder.get_object("temp_min_daily" + str(day)).set_text("Min temp: " + temp_min)

            date = str(self.api_manager.get_daily_time()[day])
            self.builder.get_object("daily_date_daily" + str(day)).set_text(date)

    # Updates all GUI elements
    def update_elements(self):
        self.update_current_elements()
        self.update_hourly_elements()
        self.update_daily_elements()

    # Loads image into GtkImage object and resizes it
    def load_image(self, image, image_file, width, height):\
        # If the file does not exist
        if not os.path.exists(image_file):
            # Show an error, stop weather,  manager and exit
            self.show_message_box(Gtk.MessageType.ERROR, "Not found: " + image_file)
            exit()

        # Load image from file
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_file)

        # Resize the image
        pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

        # Set the resized image as the source of the GtkImage widget
        image.set_from_pixbuf(pixbuf)

    # Determines which icon to use based on the weather conditions
    def set_data_image(self, image, data):
        rain = data["rain"]
        snow = data["snowfall"]
        cloudcover = data["cloudcover"]

        if rain > 0:
            self.load_image(image, self.cur_path + "/Assets/Icons/cloud_rain.png", 30, 30)
        elif snow > 0:
            self.load_image(image, self.cur_path + "/Assets/Icons/cloud_snow.png", 30, 30)
        elif cloudcover >= 30:
            self.load_image(image, self.cur_path + "/Assets/Icons/cloud.png", 30, 30)
        else:
            self.load_image(image, self.cur_path + "/Assets/Icons/sunny.png", 30, 30)

    # Loads icon for current weather data
    def load_cur_image(self):
        current_temperature = self.builder.get_object("current_weather_icon")
        self.set_data_image(current_temperature, self.api_manager.get_cur_data())

    # Loads icons for hourly forecast
    def load_hourly_image(self):
        for hour in range(24):
            weather_data = self.api_manager.get_hourly_data()
            data = {
                "rain": weather_data["rain"][hour],
                "snowfall": weather_data["snowfall"][hour],
                "cloudcover": weather_data["cloudcover"][hour]
            }
            icon = self.builder.get_object("icon_hourly" + str(hour))
            self.set_data_image(icon, data)

    # Sets exit flag and stops update thread
    def set_exit_flag(self):
        self.exit = True

    def show_message_box(self, type, message):
        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=type,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()