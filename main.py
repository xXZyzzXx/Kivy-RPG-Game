from gui import *
from screens.menu_screen import MenuScreen
from screens.main_screen import MainScreen
from screens.isomap_screen import IsoMapScreen
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, WipeTransition
from kivy.properties import ObjectProperty


class StrategyApp(App):
    def __init__(self, **kvargs):
        super(StrategyApp, self).__init__(**kvargs)
        self.config = ConfigParser()
        self.settings_popup = None
        settings_popup = ObjectProperty(None, allownone=True)

    def build(self):
        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(IsoMapScreen(name='iso_map'))
        sm.current = 'menu'  # temporary for testing
        return sm

    def on_settings_cls(self, *args):
        self.destroy_settings()

    def display_settings(self, settings):
        self.settings_popup = p = Popup(content=settings,
                                        title='Settings',
                                        size_hint=(0.8, 0.8))
        if p.content is not settings:
            p.content = settings
        p.open()

    def close_settings(self, *args):
        p = self.settings_popup
        if p is not None:
            p.dismiss()


if __name__ == '__main__':
    Window.maximize()
    StrategyApp().run()
