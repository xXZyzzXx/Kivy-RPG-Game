import additional as ad
from kivy.app import App
from kivy.config import Config
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from libraries.transitions import RVBTransition
from screens.isomap_screen import IsoMapScreen
from screens.main_screen import MainScreen
from screens.menu_screen import MenuScreen


class StrategyApp(App):
    def __init__(self, **kvargs):
        super(StrategyApp, self).__init__(**kvargs)
        self.config = ConfigParser()
        Config.set('kivy', 'exit_on_escape', '0')
        self.settings_popup = None
        settings_popup = ObjectProperty(None, allownone=True)

    def build(self):
        Window.bind(on_key_down=self.key_action)
        self.root = ScreenManager(transition=RVBTransition())  # WipeTransition()
        menu_screen = MenuScreen(name='menu')
        self.root.add_widget(menu_screen)
        self.root.add_widget(MainScreen(name='main'))
        self.root.add_widget(IsoMapScreen(name='iso_map'))
        self.root.current = 'menu'  # temporary for testing
        menu_screen.new_game()  # сразу создать новую игру
        self.root.current = 'iso_map'
        return self.root

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

    def key_action(self, window, keycode1, keycode2, text, modifiers):  # Открыть главное меню при нажатии Esc
        if keycode1 == 27:
            ad.set_screen('menu', self.root)


if __name__ == '__main__':
    Window.maximize()
    StrategyApp().run()
