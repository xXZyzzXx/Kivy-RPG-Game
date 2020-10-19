import additional as ad
import config
import data_center
from gui_list.gamebase import *
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import Screen


class MainScreen(Screen):
    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)
        self.layout = None
        self.timer_event = None
        self.money_label = None
        self.res_grid = None
        self.programs_grid = None
        self.res_label_list = None
        self.main_base = None
        self.total_programs_label = None
        self.pb_list = None
        self.player = None
        self.turn_label = None

    def on_enter(self, *args):
        self.player = config.current_player

        self.layout = RelativeLayout()
        canvas = CityCanvas()
        self.main_base = BuildingBase(id='main_base', pos_hint=({'center_x': .6, 'center_y': .42}),
                                      size_hint=(0.15, 0.15))
        navigation = BoxLayout(size_hint=(.4, .1), pos_hint=({'center_x': .5, 'top': 1}))
        stack = GridLayout(cols=4, spacing=5)
        map_button = RockLayout(MapButton(on_press=lambda x: ad.set_screen('iso_map', self.manager)))
        war_button = RockLayout(WarButton(on_press=lambda x: ad.set_screen('iso_map', self.manager)))
        report_button = RockLayout(ReportButton(on_press=lambda x: ad.set_screen('iso_map', self.manager)))
        letter_button = RockLayout(MailButton(on_press=lambda x: ad.set_screen('iso_map', self.manager)))
        stack.add_widget(war_button)
        stack.add_widget(map_button)
        stack.add_widget(report_button)
        stack.add_widget(letter_button)
        navigation.add_widget(stack)
        self.empty_space = Building(id='f1', pos_hint=({'center_x': .4, 'center_y': .2}), size_hint=(None, None))
        self.empty_space2 = Building(id='f2', pos_hint=({'center_x': .6, 'center_y': .2}), size_hint=(None, None))
        self.empty_space3 = Building(id='f3', pos_hint=({'center_x': .5, 'center_y': .3}), size_hint=(None, None))
        self.buildings = [self.empty_space, self.empty_space2, self.empty_space3]
        self.layout.add_widget(canvas)
        self.layout.add_widget(self.main_base)
        self.layout.add_widget(self.empty_space)
        self.layout.add_widget(self.empty_space2)
        self.layout.add_widget(self.empty_space3)
        self.layout.add_widget(navigation)
        self.layout.add_widget(self.test_lay())
        self.layout.add_widget(self.top_left_content())
        self.layout.add_widget(self.top_right_content())
        self.layout.add_widget(self.right_sidebar_content())

        self.update_programs()
        self.update_progressbar()
        self.layout.add_widget(self.turn_layout_content())
        self.layout.add_widget(self.next_turn_content())
        self.layout.add_widget(self.research_content())
        self.add_widget(self.layout)
        # self.timer_event = Clock.schedule_interval(lambda dt: self.update_resources(buildings), 1)

    def top_left_content(self):
        lay = LeftInfoLay(size_hint=(.3, .05), pos_hint=({'top': 1, 'x': 0}))
        lay.add_widget(Label(text='Top info text', font_size=10))
        return lay

    def top_right_content(self):
        lay = RightInfoLay(size_hint=(.3, .05), pos_hint=({'top': 1, 'right': 1}))
        lay.add_widget(Label(text='Top info text', font_size=10))
        return lay

    def research_content(self):
        left_box = BoxLayout(orientation='vertical', size_hint=(.2, .4), pos_hint=({'top': .85, 'x': 0}), spacing=20)
        tech_lay = TechLay(orientation='horizontal', size_hint_y=.5, padding=10)
        malware_lay = TechLay(size_hint_y=.5)
        malware_lay.add_widget(Label(text='Очки мутации'))
        technology_box = BoxLayout(orientation='vertical')
        technology_box.add_widget(Label(text='Текущая технология:', size_hint_y=.3))
        technology_box.add_widget(Label(text='Новые вирусы\n\n100/30 (3 хд)', size_hint_y=.7))
        tech_lay.add_widget(Image(source='data/images/gui_elements/malware1.png', size_hint=(.4, .7),
                                  pos_hint=({'center_y': .5})))
        tech_lay.add_widget(technology_box)
        left_box.add_widget(tech_lay)
        left_box.add_widget(malware_lay)
        return left_box

    def test_lay(self):
        mainmenu = BoxLayout(orientation='vertical', size_hint=(.1, .1), pos_hint=({'right': 1, 'y': 0}))
        stackscreens = GridLayout(rows=3, spacing=5)
        prod_menu_screen = Button(size_hint_x=.1, text='prod_menu', on_release=lambda x: self.prod_menu_newscreen())
        data_center_screen = Button(size_hint_x=.1, text='data_center',
                                    on_release=lambda x: self.data_center_newscreen())
        terminal_button = Button(size_hint_x=.1, text='terminal', on_release=lambda x: self.open_terminal())
        stackscreens.add_widget(prod_menu_screen)
        stackscreens.add_widget(data_center_screen)
        stackscreens.add_widget(terminal_button)
        mainmenu.add_widget(stackscreens)
        return mainmenu

    def data_center_newscreen(self):
        self.layout.add_widget(data_center.data_center_content(self.empty_space))

    def prod_menu_newscreen(self):
        self.layout.add_widget(building.prod_menu(self.empty_space2))

    def next_turn_content(self):
        next_turn_lay = NextTurnLayout(orientation='vertical', size_hint=(.12, .2), pos_hint=({'y': .15, 'x': 0}))
        turn_button = TurnButton(size_hint=(.7, .7), pos_hint=({'center_x': .5, 'center_y': .5}),
                                 on_release=lambda x: self.end_turn())
        next_turn_lay.add_widget(turn_button)

        return next_turn_lay

    def end_turn(self):
        self.update_resources(self.buildings)
        config.game.turn += 1
        self.update_turn_info()

    def update_turn_info(self):
        self.turn_label.text = f'{config.current_player.era}\nТекущий ход: {str(config.game.turn)}'

    def turn_layout_content(self):
        turn_lay = TurnLayout(orientation='vertical', size_hint=(.2, .15), pos_hint=({'top': .95, 'right': 1}))
        era = config.current_player.era
        turn = config.game.turn
        self.turn_label = Label(text=f'{era}\nТекущий ход: {turn}', font_size=18)
        turn_lay.add_widget(self.turn_label)
        return turn_lay

    # Добавление и обновление ресурсов
    def right_sidebar_content(self):
        right_sidebar = RightSidebar(orientation='vertical', size_hint=(.17, .6),
                                     pos_hint=({'center_y': .45, 'right': 1}))
        rel_res = GridLayout(cols=2, size_hint_y=.25, padding=5)
        self.res_label_list = []
        self.pb_list = []
        money = self.player.mutantcoin
        money_box = TestBoxLayout(orientation='vertical', spacing=2, padding=2)
        self.money_label = ResLabel(id='Деньги', text=f'{money[0]} [size=13]+{money[1]}[/size]')
        self.programs_grid = GridLayout(cols=1, row_default_height=30)
        money_box.add_widget(self.money_label)
        rel_res.add_widget(MoneyImage(size=(30, 30), size_hint_x=.2, source=money[2]))
        rel_res.add_widget(money_box)
        self.create_resources()
        res_box = BoxLayout(orientation='vertical', size_hint_y=.475)
        programs_box = BoxLayout(orientation='vertical', size_hint_y=.475)
        res_box.add_widget(rel_res)
        res_box.add_widget(Image(source='data/images/gui_elements/line.png', size_hint_y=.05))
        res_box.add_widget(self.res_grid)
        programs_box.add_widget(Image(source='data/images/gui_elements/line.png', size_hint_y=.05))
        programs_box.add_widget(self.create_programs_lay())
        programs_box.add_widget(self.programs_grid)
        right_sidebar.add_widget(Label(text='Ресурсы', size_hint_y=.05, color=(0, 0, 0, 1)))
        right_sidebar.add_widget(res_box)
        right_sidebar.add_widget(programs_box)
        return right_sidebar

    def create_resources(self):
        self.res_grid = GridLayout(rows=5, row_default_height=40)
        for res in self.player.resources:
            resource = self.player.resources[res]
            rel_ress = GridLayout(cols=3, size_hint_y=None, padding=5, height=40)
            resource_box = TestBoxLayout(orientation='vertical', spacing=2, padding=2)
            resource_label = ResLabel(id=f'{res}')
            if int(resource[1]) > 0:
                resource_label.text = f'{int(resource[0])} [size=13]+{resource[1]}[/size]'
            else:
                resource_label.text = f'{int(resource[0])}'
            resource_progress = ProgressBar(id=f'p_{res}', size_hint=(1, .1), max=resource[3])
            resource_box.add_widget(resource_label)
            resource_box.add_widget(resource_progress)
            rel_ress.add_widget(MoneyImage(size_hint_x=.25, source=resource[2]))
            rel_ress.add_widget(resource_box)
            max_ress = BoxLayout(orientation='horizontal', height=20, size_hint=(0.3, 1), pos_hint=({'center_y': .5}))
            max_ress.add_widget(
                LeftLabel(text=f'{resource[3]}', color=(0, 0, 0, 0.3), size_hint=(0.5, 0.5), font_size=12))
            rel_ress.add_widget(max_ress)
            self.res_grid.add_widget(rel_ress)
            self.res_label_list.append(resource_label)
            self.pb_list.append(resource_progress)

    def update_resources(self, buildings):
        money = self.player.mutantcoin
        money[0] += money[1]
        if money[1] > 0:
            self.money_label.text = f'{money[0]} [size=13]+{money[1]}[/size]'
        else:
            self.money_label.text = f'{money[0]}'
        # Обновление для сырьевых ресурсов
        for i, resource in enumerate(self.player.resources):
            res = self.player.resources[resource]
            if res[0] <= res[3] and res[0] + res[1] <= res[3]:
                res[0] += res[1]
            else:
                res[0] = res[3]
            if res[1] > 0:
                self.res_label_list[i].text = f'{int(res[0])} [size=13]+{res[1]}[/size]'
            else:
                self.res_label_list[i].text = f'{int(res[0])}'
        # Обновление для текущих программ
        self.programs_grid.clear_widgets()
        self.update_programs()
        self.update_total_programs_label()
        self.update_progressbar()
        for b in buildings:
            if b.active:
                b.update_available_units()

    def update_progressbar(self):
        for i, resource in enumerate(self.player.resources):
            res = self.player.resources[resource]
            sklad_coefficient = res[0] / res[3]
            self.pb_list[i].value_normalized = sklad_coefficient

    def update_programs(self):
        programs = self.player.programs
        for program in programs:
            if programs[program] > 0:
                program_ress = GridLayout(cols=3, size_hint_y=None, padding=5, spacing=5, height=40)
                program_image = Image(source=config.programs[program][0], size_hint_x=.2)
                program_label = ProgramSidebarLabel(text=f'{program} {programs[program]} ед.')
                program_ress.add_widget(program_image)
                program_ress.add_widget(program_label)
                self.programs_grid.add_widget(program_ress)

    def create_programs_lay(self):
        programs_lay = GridLayout(cols=3, spacing=5, padding=2, size_hint_y=.2)
        programs_layout = BoxLayout(orientation='horizontal', size_hint_x=.35)
        programs_now = 0
        programs = self.player.programs
        for pr in programs:
            programs_now += int(programs[pr]) * int(config.programs[pr][3])
        self.total_programs_label = RightLabel(text=f'{programs_now}/{self.player.programs_max}', size_hint_x=.45)
        programs_layout.add_widget(self.total_programs_label)
        img_box = BoxLayout(size_hint_x=.2)
        img_box.add_widget(
            Image(source='data/images/gui_elements/terminal_icon.png', size_hint=(.8, .8), pos_hint=({'center_y': .5})))
        programs_layout.add_widget(Image(source=r'data/images/gui_elements/disketa.png', size_hint=(.35, .4),
                                         pos_hint=({'center_x': .5, 'center_y': .5})))
        programs_lay.add_widget(img_box)
        programs_lay.add_widget(ProgramSidebarLabel(text='Программы', font_size=16, size_hint_x=.45))
        programs_lay.add_widget(programs_layout)
        return programs_lay

    def update_total_programs_label(self):
        programs_now = 0
        programs = self.player.programs
        for pr in programs:
            programs_now += int(programs[pr]) * int(config.programs[pr][3])
        self.total_programs_label.text = f'{programs_now}/{self.player.programs_max}'

    def open_terminal(self):
        scatter_terminal = ScatterLayout(size_hint=(.4, .5))
        terminal_lay = TerminalRelativeLayout()
        scroll_terminal = TerminalScrollView(size_hint=(.97, .87), pos_hint=({'center_x': .5, 'top': .9}))
        terminal_top = RelativeLayout(size_hint=(.97, .1), pos_hint=({'center_x': .5, 'top': 1}))
        terminal_top.add_widget(TerminalIcon(pos_hint=({'x': .005, 'top': 1}), size_hint_x=.04))
        terminal_top.add_widget(TerminalTitleLabel(text=r'C:\JARVIS\Terminal [Version 7.1.2336]',
                                                   pos_hint=({'x': .05, 'top': 1}), size_hint_x=.992))
        terminal_top.add_widget(
            TerminalClose(parent_lay=self.layout, close_lay=scatter_terminal, pos_hint=({'right': .99, 'top': 1}),
                          size_hint_x=.04))
        terminal_main = TerminalGridLayout(cols=1, size_hint_y=None, padding=3, spacing=5)
        terminal_main.bind(minimum_height=terminal_main.setter('height'))
        terminal_main.add_widget(
            TerminalLabel(text='JARVIS Terminal (c) Corporation JARVIS, 2044. All rights reserved'))
        terminal_main.add_widget(TerminalTextInput(grid=terminal_main))
        terminal_lay.add_widget(terminal_top)
        scroll_terminal.add_widget(terminal_main)
        terminal_lay.add_widget(scroll_terminal)
        scatter_terminal.add_widget(terminal_lay)
        self.layout.add_widget(scatter_terminal)

    def on_leave(self, *args):
        self.clear_widgets()
        Clock.unschedule(self.timer_event)
