from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen

Window.clearcolor = get_color_from_hex('#ffffff')
Window.size = (450, 600)

class Topbar_screen(MDScreen):
    pass
class Navigation_drawer(MDScreen):
    pass

class TopAppNavigation(MDApp):
    def build(self):


        kv  = Builder.load_file('topbar.kv')
        return kv



app = TopAppNavigation()
app.run()






