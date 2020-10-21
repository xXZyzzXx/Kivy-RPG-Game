import additional as ad
from tile_map import MyMap
import config
from game import Game, Player
from kivy.core.window import Window
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
        self.carousel.add_widget(self.new_game_menu())
        self.layout.add_widget(w)
        self.layout.add_widget(self.carousel)
        self.add_widget(self.layout)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def adv_menu(self):
        menu_box = MenuRelativeLayout(size_hint=(None, None), size=(600, 600), pos_hint=({'center_x': .5, 'center_y': .5}))
        menu_top = Image(source=r'data/images/menu/menu_top.png', size_hint=(None, None), size=(426, 212),
                         pos_hint=({'center_x': .5, 'top': 1}))
        menu_left = Image(source=r'data/images/menu/menu_left.png', size_hint=(None, None), size=(212, 426),
                         pos_hint=({'x': 0, 'center_y': .5}))
        menu_right = Image(source=r'data/images/menu/menu_right.png', size_hint=(None, None), size=(212, 426),
                         pos_hint=({'right': 1, 'center_y': .5}))
        menu_bottom = Image(source=r'data/images/menu/menu_bottom.png', size_hint=(None, None), size=(426, 212),
                         pos_hint=({'center_x': .5, 'y': 0}))
        menu_center = Image(source=r'data/images/menu/center.png', size_hint=(None, None), size=(250, 250),
                            pos_hint=({'center_x': .5, 'center_y': .5}))
        menu_box.add_widget(menu_top)
        menu_box.add_widget(menu_left)
        menu_box.add_widget(menu_right)
        menu_box.add_widget(menu_bottom)
        menu_box.add_widget(menu_center)
        return menu_box

    def menu(self):
        menu_box = GridLayout(cols=1, size_hint=(.4, .5), pos_hint=({'center_x': .5, 'center_y': .5}), spacing=10)
        continue_button = Button(text='Продолжить', size_hint_y=.2, disabled=True)
        start_button = Button(text='Новая игра', size_hint_y=.2, on_release=lambda x: self.carousel.load_next(mode='next'))
        load_button = Button(text='Загрузить игру', size_hint_y=.2,
                             on_release=lambda x: ad.set_screen('iso_map', self.manager))
        if config.game is None:
            load_button.disabled = True
        settings_button = Button(text='Настройки', size_hint_y=.2, on_release=lambda x: self.open_settings())
        exit_button = Button(text='Выйти из игры', size_hint_y=.2, on_release=lambda x: self.close_app())
        menu_box.add_widget(continue_button)
        menu_box.add_widget(start_button)
        menu_box.add_widget(load_button)
        menu_box.add_widget(settings_button)
        menu_box.add_widget(exit_button)
        return menu_box

    def new_game_menu(self):
        box = BoxLayout(orientation='vertical', size_hint=(.7, .8), pos_hint=({'center_x': .5, 'center_y': .5}))
        left_box = BoxLayout(orientation='vertical', size_hint_x=.3)
        right_box = BoxLayout(orientation='vertical', size_hint_x=.7)
        top_box = BoxLayout(orientation='horizontal', size_hint_y=.85)
        bottom_box = DescBottomLayout(size_hint_y=.15)
        map_lay = MapBoxLayout(orientation='horizontal', size_hint_y=.5)
        map_description = DescBoxLayout(orientation='horizontal', size_hint_y=.35)
        # =======================================
        map_exs = MyMap()
        map_img = Image(source=map_exs.screen, size_hint_x=.8)
        left_map = Button(text='<', size_hint_x=.1)  # , disabled=True
        right_map = Button(text='>', size_hint_x=.1)  # , disabled=True
        map_lay.add_widget(left_map)
        map_lay.add_widget(map_img)
        map_lay.add_widget(right_map)
        # =======================================
        desc_label = DescLabel(text='Описание', size_hint_y=.05, valign='bottom')
        desc_grid_left = GridLayout(cols=1, size_hint_x=.3, padding=10)
        desc_grid_right = GridLayout(cols=1, size_hint_x=.7, padding=10)
        desc_grid_left.add_widget(Label(text='Название карты:'))
        desc_grid_right.add_widget(Label(text=f'{map_exs.source.split("/")[-1]}'))
        desc_grid_left.add_widget(Label(text='Размер карты:'))
        desc_grid_right.add_widget(Label(text=f'{map_exs.map_width}x{map_exs.map_height}'))
        desc_grid_left.add_widget(Label(text='Игроков:'))
        desc_grid_right.add_widget(Label(text=f'{map_exs.players}'))
        map_description.add_widget(desc_grid_left)
        map_description.add_widget(desc_grid_right)
        # =======================================
        right_box.add_widget(DescLabel(text='Выбор карты', size_hint_y=.1))
        right_box.add_widget(map_lay)
        right_box.add_widget(desc_label)
        right_box.add_widget(map_description)
        # =======================================
        left_box.add_widget(DescLabel(text='Настройки игры', size_hint_y=.1))
        settings_box = SettingsLayout(size_hint_y=.9)
        left_box.add_widget(settings_box)
        # =======================================
        bottom_box.add_widget(Button(size_hint=(.2, .7), pos_hint=({'x': 0, 'center_y': .5}),
                                     on_release=lambda x: self.carousel.load_previous(), text='<= Назад'))

        bottom_box.add_widget(Button(size_hint=(.3, .7), pos_hint=({'center_x': .5, 'center_y': .5}),
                              on_release=lambda x: self.new_game(), text='Начать игру'))

        bottom_box.add_widget(Button(size_hint=(.2, .7), pos_hint=({'right': 1, 'center_y': .5}),
                                     on_release=lambda x: self.map_settings(), text='Настройки карты'))
        # =======================================
        top_box.add_widget(left_box)
        top_box.add_widget(right_box)
        box.add_widget(top_box)
        box.add_widget(bottom_box)
        return box

    def new_game(self):
        game = Game()
        player1 = Player(player=True)  # TODO: город добавить тут
        player1.add_city((17, 17), name='Персеполис')
        player2 = Player()
        player2.add_city((3, 41), name='Научград')
        game.players = [player1, player2]
        config.game = game
        config.current_player = player1
        ad.set_screen('main', self.manager)

    def open_settings(self):
        self.app.destroy_settings()
        self.app.settings_cls = SettingsWithSidebar
        self.app.open_settings()

    def map_settings(self):
        popup = Popup(title='Настройки карты', content=Label(text='В разработке'), size_hint=(.4, .5))
        popup.open()

    def close_app(self):
        self.app.stop()

    def on_mouse_pos(self, window, pos):
        '''
        x, y = self.menu.pos
        menuX, menuY = pos
        posX = menuX-x
        posY = menuY-y
        cellX = self.menu.width / 3
        cellY = self.menu.height / 3
        print(f'{posX, posY} | {posX % cellX} | {posY % cellY}')
        '''
        pass

    def on_leave(self, *args):
        self.layout.clear_widgets()


class MenuCarousel(Carousel):
    def __init__(self, **kwargs):
        super(MenuCarousel, self).__init__(**kwargs)

    def on_touch_move(self, touch):  # Переопределение (не разрешать двигать табуретками)
        pass


class MenuRelativeLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(MenuRelativeLayout, self).__init__(**kwargs)


class DescBoxLayout(BoxLayout):
    pass


class DescLabel(Label):
    pass


class MapBoxLayout(BoxLayout):
    pass


class DescBottomLayout(RelativeLayout):
    pass


class SettingsLayout(BoxLayout):
    pass