from gui import *
from screens.menu_screen import MenuScreen
from screens.main_screen import MainScreen
from screens.isomap_screen import IsoMapScreen
import additional as ad
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, WipeTransition
from kivy.properties import ObjectProperty


class StrategyApp(App):
    def __init__(self, **kvargs):
        super(StrategyApp, self).__init__(**kvargs)
        self.config = ConfigParser()
        Config.set('kivy', 'exit_on_escape', '0')
        self.settings_popup = None
        self.sm = None
        settings_popup = ObjectProperty(None, allownone=True)

    def build(self):
        Window.bind(on_key_down=self.key_action)
        self.sm = ScreenManager(transition=WipeTransition())
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(IsoMapScreen(name='iso_map'))
        self.sm.current = 'menu'  # temporary for testing
        return self.sm

    def on_settings_cls(self, *args):
        self.destroy_settings()

    def display_settings(self, settings):
        self.settings_popup = p = Popup(content=settings, title='Settings', size_hint=(0.7, 0.8))
        if p.content is not settings:
            p.content = settings
        p.open()

    def close_settings(self, *args):
        p = self.settings_popup
        if p is not None:
            p.dismiss()

    def key_action(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 == 27:
            ad.set_screen('menu', self.sm)


if __name__ == '__main__':
    Window.maximize()
    StrategyApp().run()
