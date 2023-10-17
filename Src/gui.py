import gi
# If multiple versions of GTK installed, make sure 3.0 is installed as well
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from WeatherManager import WeatherManager
import os

class GUIManager:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("Py-Weather-GUI.glade")
        window = builder.get_object("main_window")
        window.show_all()
        Gtk.main()

gui=GUIManager()