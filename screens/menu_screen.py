import additional as ad
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image, AsyncImage
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.effectwidget import EffectWidget, FXAAEffect
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen


class MenuScreen(Screen):
    def __init__(self, **kw):
        super(MenuScreen, self).__init__(**kw)
        self.layout = None
        self.carousel = None
        self.app = App.get_running_app()

    def on_enter(self, *args):
        self.layout = RelativeLayout()
        self.carousel = MenuCarousel(direction='right')
        w = EffectWidget()
        bg = Image(source='data/images/animation.zip', allow_stretch=True, keep_ratio=False)
        w.add_widget(bg)
        w.effects = [FXAAEffect()]
        self.carousel.add_widget(self.menu())
        self.carousel.add_widget(self.new_game())
        self.layout.add_widget(w)
        self.layout.add_widget(self.carousel)
        self.add_widget(self.layout)

    def menu(self):
        menu_box = GridLayout(cols=1, size_hint=(.4, .5), pos_hint=({'center_x': .5, 'center_y': .5}), spacing=10)
        continue_button = Button(text='Продолжить', size_hint_y=.2, disabled=True)
        start_button = Button(text='Новая игра', size_hint_y=.2, on_release=lambda x: self.carousel.load_next(mode='next'))
        load_button = Button(text='Загрузить игру', size_hint_y=.2,
                             on_release=lambda x: ad.set_screen('iso_map', self.manager))
        settings_button = Button(text='Настройки', size_hint_y=.2, on_release=lambda x: self.open_settings())
        exit_button = Button(text='Выйти из игры', size_hint_y=.2, on_release=lambda x: self.close_app())
        menu_box.add_widget(continue_button)
        menu_box.add_widget(start_button)
        menu_box.add_widget(load_button)
        menu_box.add_widget(settings_button)
        menu_box.add_widget(exit_button)
        return menu_box

    def new_game(self):
        box = BoxLayout(orientation='vertical', size_hint=(.7, .8), pos_hint=({'center_x': .5, 'center_y': .5}))
        left_box = BoxLayout(size_hint_x=.3)
        right_box = BoxLayout(size_hint_x=.7)
        top_box = BoxLayout(orientation='horizontal', size_hint_y=.85)
        bottom_box = RelativeLayout(size_hint_y=.15)
        bottom_box.add_widget(Button(size_hint=(.3, .7), pos_hint=({'center_x': .5, 'center_y': .5}),
                              on_release=lambda x: self.carousel.load_previous(), text='Начать игру'))
        top_box.add_widget(left_box)
        top_box.add_widget(right_box)
        box.add_widget(top_box)
        box.add_widget(bottom_box)
        return box

    def open_settings(self):
        self.app.destroy_settings()
        self.app.settings_cls = SettingsWithSidebar
        self.app.open_settings()

    def close_app(self):
        self.app.stop()

    def on_leave(self, *args):
        self.layout.clear_widgets()


class MenuCarousel(Carousel):
    def __init__(self, **kwargs):
        super(MenuCarousel, self).__init__(**kwargs)

    def on_touch_move(self, touch):  # Переопределение (не разрешать двигать табуретками)
        pass
