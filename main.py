import config
import data_center
from gui import *
# CityCanvas, RockLayout, MapButton, WarButton, ReportButton, MailButton, RightSidebar, FoundamentButton, MenuLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition


def set_screen(name_screen, sm):
    sm.current = name_screen


class MainScreen(Screen):
    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)
        self.layout = None
        self.timer_event = None
        self.money_label = None
        self.res_grid = None

    def on_enter(self, *args):
        self.layout = RelativeLayout()
        canvas = CityCanvas()
        # Выбор окна в главном меню
        mainmenu = BoxLayout(orientation='vertical', size_hint=(.1, .1), pos_hint=({'x': 0, 'top': 0.5}))
        stackscreens = GridLayout(rows=3, spacing=5)
        prod_menu_screen = Button(size_hint_x=.1, text='prod_menu', on_release=lambda x: self.prod_menu_newscreen())
        data_center_screen = Button(size_hint_x=.1, text='data_center',
                                    on_release=lambda x: self.data_center_newscreen())
        terminal_button = Button(size_hint_x=.1, text='terminal', on_release=lambda x: self.open_terminal())
        stackscreens.add_widget(prod_menu_screen)
        stackscreens.add_widget(data_center_screen)
        stackscreens.add_widget(terminal_button)
        navigation = BoxLayout(size_hint=(.4, .11), pos_hint=({'center_x': .5, 'top': 1}))
        stack = GridLayout(cols=4, spacing=5)
        map_button = RockLayout(MapButton(on_press=lambda x: set_screen('iso_map', self.manager)))
        war_button = RockLayout(WarButton(on_press=lambda x: set_screen('iso_map', self.manager)))
        report_button = RockLayout(ReportButton(on_press=lambda x: set_screen('iso_map', self.manager)))
        letter_button = RockLayout(MailButton(on_press=lambda x: set_screen('iso_map', self.manager)))
        stack.add_widget(war_button)
        stack.add_widget(map_button)
        stack.add_widget(report_button)
        stack.add_widget(letter_button)
        navigation.add_widget(stack)
        mainmenu.add_widget(stackscreens)
        self.empty_space = Building(id='f1', pos_hint=({'center_x': .4, 'center_y': .1}), size_hint=(None, None))
        self.empty_space2 = Building(id='f2', pos_hint=({'center_x': .6, 'center_y': .1}), size_hint=(None, None))
        buildings = [self.empty_space, self.empty_space2]
        self.layout.add_widget(canvas)
        self.layout.add_widget(self.empty_space)
        self.layout.add_widget(self.empty_space2)
        self.layout.add_widget(navigation)
        self.layout.add_widget(mainmenu)
        self.layout.add_widget(self.right_sidebar_content())
        self.add_widget(self.layout)
        # building.menu_content(empty_space)
        # empty_space.name = 'Казармы'  # For testing
        # empty_space.active = True
        # self.layout.add_widget(empty_space.building_content(build_place=self, build='Казармы'))  # For testing
        # self.layout.add_widget(building.prod_menu(empty_space2))

        self.timer_event = Clock.schedule_interval(
            lambda dt: self.update_resources(self.res_label_list, self.pb_list, buildings), 1)

    def data_center_newscreen(self):
        self.layout.add_widget(data_center.data_center_content(self.empty_space))

    def prod_menu_newscreen(self):
        self.layout.add_widget(building.prod_menu(self.empty_space2))

    def open_terminal(self):
        scatter_terminal = ScatterLayout(size_hint=(.4, .5))
        terminal_lay = TerminalRelativeLayout()
        scroll_terminal = TerminalScrollView(size_hint=(.97, .87), pos_hint=({'center_x': .5, 'top': .9}))
        terminal_top = RelativeLayout(size_hint=(.97, .1), pos_hint=({'center_x': .5, 'top': 1}))
        terminal_top.add_widget(TerminalIcon(pos_hint=({'x': .005, 'top': 1}), size_hint_x=.04))
        terminal_top.add_widget(TerminalTitleLabel(text=r'C:\JARVIS\Terminal [Version 7.1.2336]',
                                                   pos_hint=({'x': .05, 'top': 1}), size_hint_x=.992))
        terminal_top.add_widget(TerminalClose(pos_hint=({'right': .99, 'top': 1}), size_hint_x=.04))
        terminal_main = TerminalGridLayout(cols=1, size_hint_y=None, padding=3, spacing=5)
        terminal_main.bind(minimum_height=terminal_main.setter('height'))
        terminal_main.add_widget(TerminalLabel(text='JARVIS Terminal (c) Corporation JARVIS, 2044. All rights reserved'))
        terminal_main.add_widget(TerminalTextInput(grid=terminal_main))
        terminal_lay.add_widget(terminal_top)
        scroll_terminal.add_widget(terminal_main)
        terminal_lay.add_widget(scroll_terminal)
        scatter_terminal.add_widget(terminal_lay)
        self.layout.add_widget(scatter_terminal)

    def update_resources(self, res_label_list, pb_list, buildings):
        money = config.money
        money[0] += money[1]
        if money[1] > 0:
            self.money_label.text = f'{money[0]} [size=13]+{money[1]}[/size]'
        else:
            self.money_label.text = f'{money[0]}'

        # Обновление для сырьевых ресурсов
        for i, resource in enumerate(config.resourses):
            if config.resourses[resource][0] <= config.sklad and config.resourses[resource][0] + \
                    config.resourses[resource][1] <= config.sklad:
                config.resourses[resource][0] += config.resourses[resource][1]
            else:
                config.resourses[resource][0] = config.sklad
            res = config.resourses[resource]
            if res[1] > 0:
                res_label_list[i].text = f'{int(res[0])} [size=13]+{res[1]}[/size]'
            else:
                res_label_list[i].text = f'{int(res[0])}'
            sklad_coefficient = res[0] / config.sklad
            pb_list[i].value_normalized = sklad_coefficient

        for b in buildings:
            if b.active:
                b.update_available_units()

    # Добавление и обовление ресурсов
    def right_sidebar_content(self):
        right_sidebar = RightSidebar(orientation='vertical', size_hint=(.17, .6),
                                     pos_hint=({'center_y': .5, 'right': 1}))
        rel_res = GridLayout(cols=2, size_hint_y=.15, padding=5)
        money = config.money
        money_box = TestBoxLayout(orientation='vertical', spacing=2, padding=2)
        self.money_label = ResLabel(id='Деньги', text=f'{money[0]} [size=13]+{money[1]}[/size]')
        self.res_label_list = []
        self.pb_list = []
        money_box.add_widget(self.money_label)
        rel_res.add_widget(MoneyImage(size=(30, 30), size_hint_x=.2, source=money[2]))
        rel_res.add_widget(money_box)
        self.res_grid = GridLayout(rows=5, row_default_height=30)
        for res in config.resourses:
            resource = config.resourses[res]
            sklad_coefficient = resource[0] / config.sklad
            rel_ress = GridLayout(cols=2, size_hint_y=None, padding=5, height=40)
            resource_box = TestBoxLayout(orientation='vertical', spacing=2, padding=2)
            resource_label = ResLabel(id=f'{res}', text=f'{int(resource[0])} [size=13]+{resource[1]}[/size]')
            resource_progress = ProgressBar(id=f'p_{res}', size_hint=(.9, .1), max=config.sklad)
            resource_progress.value_normalized = sklad_coefficient
            resource_box.add_widget(resource_label)
            resource_box.add_widget(resource_progress)
            rel_ress.add_widget(MoneyImage(size_hint_x=.25, source=resource[2]))
            rel_ress.add_widget(resource_box)
            self.res_grid.add_widget(rel_ress)
            self.res_label_list.append(resource_label)
            self.pb_list.append(resource_progress)
        right_sidebar.add_widget(Label(text='Ресурсы', size_hint_y=.13, color=(0, 0, 0, 1)))
        right_sidebar.add_widget(rel_res)
        right_sidebar.add_widget(Image(source='data/images/gui_elements/line.png', size_hint_y=.05))
        right_sidebar.add_widget(self.res_grid)
        right_sidebar.add_widget(SkladLabel(text=f'Склад: {config.sklad}', size_hint_y=.1, color=(0, 0, 0, 1)))
        return right_sidebar

    def on_leave(self, *args):
        self.clear_widgets()
        Clock.unschedule(self.timer_event)


class IsoMapScreen(Screen):
    def __init__(self, **kw):
        super(IsoMapScreen, self).__init__(**kw)
        self.layout = None

    def on_enter(self, *args):
        self.layout = RelativeLayout()
        navigation = BoxLayout(orientation='vertical', size_hint=(.5, None), pos_hint=({'center_x': .5, 'top': 1}),
                               height=100)
        navigation.add_widget(Button(text='Переключить на город',
                                     on_press=lambda x: set_screen('main', self.manager)))
        self.layout.add_widget(navigation)
        self.add_widget(self.layout)

    def on_leave(self, *args):
        self.clear_widgets()


class StrategyApp(App):
    def __init__(self, **kvargs):
        super(StrategyApp, self).__init__(**kvargs)
        self.config = ConfigParser()

    def build(self):
        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(IsoMapScreen(name='iso_map'))
        return sm


if __name__ == '__main__':
    Window.maximize()
    StrategyApp().run()
