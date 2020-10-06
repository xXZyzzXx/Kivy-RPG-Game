from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen


class MenuScreen(Screen):
    def __init__(self, **kw):
        super(MenuScreen, self).__init__(**kw)
        self.layout = None
        self.app = App.get_running_app()

    def on_enter(self, *args):
        self.layout = RelativeLayout()
        menu_box = GridLayout(cols=1, size_hint=(.4, .5), pos_hint=({'center_x': .5, 'center_y': .5}), spacing=10)
        continue_button = Button(text='Продолжить', size_hint_y=.2, disabled=True)
        start_button = Button(text='Новая игра', size_hint_y=.2)
        load_button = Button(text='Загрузить игру', size_hint_y=.2)
        settings_button = Button(text='Настройки', size_hint_y=.2, on_release=lambda x: self.open_settings())
        exit_button = Button(text='Выйти из игры', size_hint_y=.2, on_release=lambda x: self.close_app())
        menu_box.add_widget(continue_button)
        menu_box.add_widget(start_button)
        menu_box.add_widget(load_button)
        menu_box.add_widget(settings_button)
        menu_box.add_widget(exit_button)
        self.layout.add_widget(menu_box)
        self.add_widget(self.layout)

    def open_settings(self):
        self.app.settings_cls = SettingsWithSidebar
        self.app.open_settings()

    def close_app(self):
        self.app.stop()

    def on_leave(self, *args):
        self.layout.clear_widgets()