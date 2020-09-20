import building
import config
from additional import *
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.togglebutton import ToggleButton


def data_center_content(build_place):
    scatter, icon_box, statistic_grid, right_box = building.base_window(build_place)
    # RightBox(tab) content ===========
    data_center_panel = TabbedPanel(do_default_tab=False)
    defence_tab = DefPanelItem(icon_box, statistic_grid, text='Защита')
    defence_tab.content = tab_defence_content(defence_tab)
    hack_tab = HackPanelItem(icon_box, statistic_grid, text='Взлом')
    hack_tab.content = tab_hack_content()
    dev_tab = DevPanelItem(icon_box, statistic_grid, text='Разработка')
    dev_tab.content = tab_dev_content()
    upgrade_tab = UpgradePanelItem(icon_box, statistic_grid, text='Улучшения')
    data_center_panel.add_widget(defence_tab)
    data_center_panel.add_widget(hack_tab)
    data_center_panel.add_widget(dev_tab)
    data_center_panel.add_widget(upgrade_tab)
    defence_tab.on_press()  # Инициализация icon_box and statistic_grid
    right_box.add_widget(data_center_panel)
    return scatter


#  TAB HACK CONTENT =====================================================================
def tab_hack_content():
    lay_list = []  # TODO: добавить по нажатию на слой ProgramLayout открытие инфы
    scroll = ScrollView()
    top_program_box = BoxLayout(orientation='vertical', spacing=10)
    programs_grid = ProgramGridLayout(cols=1, spacing=5, size_hint_y=None)
    programs_grid.bind(minimum_height=programs_grid.setter('height'))
    programs_filter_box = BoxLayout(orientation='horizontal', height=50, size_hint_y=None)
    filter_title = Label(text='Фильтр: ')
    toggles_layout = BoxLayout(orientation='horizontal', padding=7, spacing=5)
    # TODO: заменить на картинки с toggle_behavior
    tg1 = HackToggleButton(programs_grid, lay_list, text='Видимый', group='hack_filter')
    tg2 = HackToggleButton(programs_grid, lay_list, text='Скрытный', group='hack_filter')
    tg3 = HackToggleButton(programs_grid, lay_list, text='Все', group='hack_filter', state='down')
    toggles_layout.add_widget(tg1)
    toggles_layout.add_widget(tg2)
    toggles_layout.add_widget(tg3)
    programs_filter_box.add_widget(filter_title)
    programs_filter_box.add_widget(toggles_layout)
    tg3.on_press()
    # TODO: добавить отображение недоступных программ внизу списка
    programs_grid.lay_list = lay_list
    scroll.add_widget(programs_grid)
    top_program_box.add_widget(programs_filter_box)
    top_program_box.add_widget(scroll)
    return top_program_box


def tab_hack_row(programs_grid, program_name, program, lay_list):
    upper_lay = BoxLayout(orientation='vertical', height=80, size_hint_y=None)
    top_box = ProgramLayout(orientation='horizontal', height=80, size_hint_y=None, upper_lay=upper_lay,
                            program=program, programs_grid=programs_grid)
    lay_list.append(top_box)
    image_lay = BoxLayout(size_hint_x=.20, padding=5)
    image_lay.add_widget(Image(source=program[0]))
    title_box = BoxLayout(orientation='vertical', size_hint_x=.60)
    title_label = Label(text=f'{program_name}')
    title_box.add_widget(title_label)
    upgrade_button = Button(text='Up', size_hint_x=.1)
    top_box.add_widget(image_lay)
    top_box.add_widget(title_box)
    top_box.add_widget(upgrade_button)
    upper_lay.add_widget(top_box)
    programs_grid.add_widget(upper_lay)


# TAB DEF CONTENT ==========================================================================
def tab_defence_content(defence_tab):
    lay_list = []  # TODO: добавить по нажатию на слой ProgramLayout открытие инфы
    scroll = ScrollView()
    top_program_box = BoxLayout(orientation='vertical', spacing=10)
    programs_grid = ProgramGridLayout(cols=1, spacing=5, size_hint_y=None)
    programs_grid.bind(minimum_height=programs_grid.setter('height'))
    programs_filter_box = BoxLayout(orientation='horizontal', height=50, size_hint_y=None)
    mode_box = BoxLayout()
    filter_title = Label(text='Режимы антивируса ')
    info_img = InfoImage(size_hint=(.18, .5), pos_hint=({'x': 0, 'center_y': .5}), info='Защита от взлома')
    mode_box.add_widget(filter_title)
    mode_box.add_widget(info_img)
    toggles_layout = BoxLayout(orientation='horizontal', padding=7, spacing=5)
    # TODO: заменить на картинки с toggle_behavior
    tg1 = DefToggleButton(defence_tab=defence_tab, text='Видимый', group='def_filter')
    tg2 = DefToggleButton(defence_tab=defence_tab, text='Скрытный', group='def_filter')
    tg3 = DefToggleButton(defence_tab=defence_tab, text='Авто', group='def_filter', disabled=True)
    toggles_layout.add_widget(tg1)
    toggles_layout.add_widget(tg2)
    toggles_layout.add_widget(tg3)
    programs_filter_box.add_widget(mode_box)
    programs_filter_box.add_widget(toggles_layout)
    for antimalware_upgrade_name in config.antimalware_upgrades:
        antimalware_upgrade = config.antimalware_upgrades[antimalware_upgrade_name]
        upper_lay = BoxLayout(orientation='vertical', height=80, size_hint_y=None)
        top_box = ProgramLayout(orientation='horizontal', height=80, size_hint_y=None, upper_lay=upper_lay,
                                program=antimalware_upgrade, programs_grid=programs_grid)
        lay_list.append(top_box)
        image_lay = BoxLayout(size_hint_x=.20, padding=5)
        image_rel = RelativeLayout()
        image_rel.add_widget(Image(source=antimalware_upgrade[0]))
        image_rel.add_widget(Label(text=f'{str(antimalware_upgrade[3])}', size=(10, 10), pos_hint=({'right': 1, 'y':0}), size_hint=(None, None)))
        image_lay.add_widget(image_rel)
        title_box = BoxLayout(orientation='vertical', size_hint_x=.60)
        title_label = Label(
            text=f'{antimalware_upgrade_name}, {antimalware_upgrade[1]}, +{antimalware_upgrade[2][0]}, +{antimalware_upgrade[2][1]}%')
        title_box.add_widget(title_label)
        upgrade_button = Button(text='Up', size_hint_x=.1)
        top_box.add_widget(image_lay)
        top_box.add_widget(title_box)
        top_box.add_widget(upgrade_button)
        upper_lay.add_widget(top_box)
        programs_grid.add_widget(upper_lay)
    programs_grid.lay_list = lay_list
    scroll.add_widget(programs_grid)
    top_program_box.add_widget(programs_filter_box)
    top_program_box.add_widget(scroll)
    return top_program_box


# Dev content =====================================================================================
def tab_dev_content():
    scroll = DevScrollView(do_scroll_x=False, scroll_x=.5, scroll_y=1)
    main_rel_layout = ProgramsRelativeLayout(height=500, width=600, size_hint=(1, 1))
    dev_item1 = DevItemIcon(pos_hint=({'center_x': .5, 'top': .95}))
    dev_item2 = DevItemIcon(pos_hint=({'center_x': .2, 'top': .60}))
    dev_item3 = DevItemIcon(pos_hint=({'center_x': .4, 'top': .60}))
    dev_item4 = DevItemIcon(pos_hint=({'center_x': .6, 'top': .60}))
    dev_item5 = DevItemIcon(pos_hint=({'center_x': .8, 'top': .60}))
    dev_item6 = DevItemIcon(pos_hint=({'center_x': .3, 'top': .25}), disabled=True)
    dev_item7 = DevItemIcon(pos_hint=({'center_x': .7, 'top': .25}), disabled=True)
    dev_item1.add_widget(Image(source=r'data/images/gui_elements/malware2.png'))
    dev_item2.add_widget(
        Image(source=r'data/images/gui_elements/building_tools.png', keep_ratio=False, allow_stretch=True))
    dev_item3.add_widget(
        Image(source=r'data/images/gui_elements/malware3.png', keep_ratio=False, allow_stretch=True))
    dev_item5.add_widget(
        Image(source=r'data/images/gui_elements/malware1.png', keep_ratio=False, allow_stretch=True))
    dev_item6.add_widget(
        Image(source=r'data/images/gui_elements/data_center.png', keep_ratio=False, allow_stretch=True))
    # Left
    gifline1 = GifLineHorizontal(pos_hint=({'center_x': .415, 'top': .85}), size_hint_x=.03)
    gifline2 = GifLineVertical(pos_hint=({'center_x': .4, 'top': .85}), size_hint_y=.25)
    gifline3 = GifLineHorizontal(pos_hint=({'center_x': .3, 'top': .7}), size_hint_x=.2)
    gifline4 = GifLineVertical(pos_hint=({'center_x': .2, 'top': .7}), size_hint_y=.1)
    additional_line1 = GifLineVertical(pos_hint=({'center_x': .4, 'top': .7}), size_hint_y=.3725)
    additional_line2 = GifLineVertical(pos_hint=({'center_x': .2, 'top': .7}), size_hint_y=.3725)
    # Right
    gifline5 = GifLineHorizontal(pos_hint=({'center_x': .585, 'top': .85}), size_hint_x=.03)
    gifline6 = GifLineVertical(pos_hint=({'center_x': .6, 'top': .85}), size_hint_y=.25)
    gifline7 = GifLineHorizontal(pos_hint=({'center_x': .7, 'top': .7}), size_hint_x=.2)
    gifline8 = GifLineVertical(pos_hint=({'center_x': .8, 'top': .7}), size_hint_y=.1)
    # Bottom Left
    gifline9 = GifLineVertical(pos_hint=({'center_x': .2, 'top': .4}), size_hint_y=.075)
    gifline10 = GifLineVertical(pos_hint=({'center_x': .4, 'top': .4}), size_hint_y=.075)
    gifline11 = GifLineHorizontal(pos_hint=({'center_x': .3, 'top': .325}), size_hint_x=.2)
    gifline12 = GifLineVertical(pos_hint=({'center_x': .3, 'top': .325}), size_hint_y=.075)

    main_rel_layout.add_widget(gifline4)
    main_rel_layout.add_widget(gifline3)
    main_rel_layout.add_widget(gifline2)
    main_rel_layout.add_widget(gifline1)
    main_rel_layout.add_widget(gifline5)
    main_rel_layout.add_widget(gifline6)
    main_rel_layout.add_widget(gifline7)
    main_rel_layout.add_widget(gifline8)
    main_rel_layout.add_widget(gifline9)
    main_rel_layout.add_widget(gifline10)
    #
    main_rel_layout.add_widget(additional_line1)
    main_rel_layout.add_widget(additional_line2)
    #
    main_rel_layout.add_widget(gifline12)
    main_rel_layout.add_widget(gifline11)
    main_rel_layout.add_widget(dev_item1)
    main_rel_layout.add_widget(dev_item2)
    main_rel_layout.add_widget(dev_item3)
    main_rel_layout.add_widget(dev_item4)
    main_rel_layout.add_widget(dev_item5)
    main_rel_layout.add_widget(dev_item6)
    main_rel_layout.add_widget(dev_item7)
    scroll.add_widget(main_rel_layout)

    return scroll


# END =============================================================================================


class DefToggleButton(ToggleButton):  # TODO: заменить на картинку с ToggleBehavior
    def __init__(self, defence_tab, **kwargs):
        super(DefToggleButton, self).__init__(**kwargs)
        self.defence_tab = defence_tab

    def on_press(self):  # TODO: Stealth/main toggle
        cyberdef_base = config.data_center['Защита']
        if self.text == 'Скрытный' and self.state == 'down':
            total_percent = cyberdef_base[1][2] + config.percent_amount
            cur_stealh_defence = int(cyberdef_base[1][1] + (cyberdef_base[1][1] * (total_percent/100)))
            cyberdef_base[1][0] = cur_stealh_defence
            self.defence_tab.stealth_label.text = f"Стелс защита: {str(cur_stealh_defence)}(+{str(total_percent)}%)"
        else:
            cyberdef_base[1][0] = cyberdef_base[1][1]
            self.defence_tab.stealth_label.text = f"Стелс защита: {str(cyberdef_base[1][1])}"
        if self.text == 'Видимый' and self.state == 'down':
            total_percent = cyberdef_base[2][2] + config.percent_amount
            cur_active_defence = int(cyberdef_base[2][1] + (cyberdef_base[2][1] * (total_percent/100)))
            cyberdef_base[2][0] = cur_active_defence
            self.defence_tab.active_def_label.text = f"Активная защита: {str(cur_active_defence)}(+{str(total_percent)}%)"
        else:
            self.defence_tab.active_def_label.text = f"Активная защита: {str(cyberdef_base[2][1])}"


class HackToggleButton(ToggleButton):  # TODO: заменить на картинку с ToggleBehavior
    def __init__(self, programs_grid, lay_list, **kwargs):
        super(HackToggleButton, self).__init__(**kwargs)
        self.programs_grid = programs_grid
        self.lay_list = lay_list

    def on_press(self):
        self.programs_grid.clear_widgets()
        for program_name in config.programs:
            program = config.programs[program_name]
            if self.text == 'Все':
                tab_hack_row(self.programs_grid, program_name, program, self.lay_list)
            elif program[2] == self.text:
                tab_hack_row(self.programs_grid, program_name, program, self.lay_list)
        # TODO: добавить отображение недоступных программ внизу списка
        self.programs_grid.lay_list = self.lay_list


class DevToggleButton(ToggleButton):  # TODO: заменить на картинку с ToggleBehavior
    def __init__(self, **kwargs):
        super(DevToggleButton, self).__init__(**kwargs)

    def on_press(self):
        pass


class HackPanelItem(TabbedPanelItem):
    def __init__(self, icon_box, statistic_grid, **kwargs):
        super(HackPanelItem, self).__init__(**kwargs)
        self.icon_box = icon_box
        self.statistic_grid = statistic_grid

    def on_press(self):
        self.icon_box.clear_widgets()
        self.icon_box.add_widget(Image(source=config.data_center[self.text][0]))  # TODO: добавить анимацию перехода
        self.statistic_grid.clear_widgets()
        queue_box = BoxLayout(orientation='horizontal', size_hint_y=.4)  # TODO: кастомизировать очередь
        queue_box.add_widget(Label(text='Очередь: '))
        compile_box = GridLayout(cols=2, size_hint_y=.6)  # TODO: кастомизировать слоты компиляции
        for i in range(4):
            compile_box.add_widget(Image(source=r'data/images/gui_elements/empty_icon.png'))
        self.statistic_grid.add_widget(queue_box)
        self.statistic_grid.add_widget(compile_box)


class DefPanelItem(TabbedPanelItem):
    def __init__(self, icon_box, statistic_grid, **kwargs):
        super(DefPanelItem, self).__init__(**kwargs)
        self.icon_box = icon_box
        self.statistic_grid = statistic_grid
        self.stealth_label = None
        self.active_def_label = None

    def on_press(self):
        self.icon_box.clear_widgets()
        self.icon_box.add_widget(Image(source=config.data_center[self.text][0]))  # TODO: добавить анимацию перехода
        self.statistic_grid.clear_widgets()
        stat_grid = GridLayout(cols=1, size_hint_y=.4)
        cyberdef_base = config.data_center['Защита']
        self.active_def_label = DefAmountLabel(text=f"Активная защита: {str(cyberdef_base[2][1])}", font_size=14)
        self.stealth_label = DefAmountLabel(text=f"Стелс защита: {str(cyberdef_base[1][1])}", font_size=14)
        stat_grid.add_widget(self.active_def_label)
        stat_grid.add_widget(self.stealth_label)
        antivirus_box = BoxLayout(orientation='vertical', size_hint_y=.6)
        antivirus_label = Label(text='Разработка', size_hint_y=.2)
        antivirus_icon = Image(source=config.current_antivirus_tech[1], size_hint_y=.6)
        antivirus_progress = Label(text=config.current_antivirus_tech[2], size_hint_y=.2)
        antivirus_box.add_widget(antivirus_label)
        antivirus_box.add_widget(antivirus_icon)
        antivirus_box.add_widget(antivirus_progress)
        self.statistic_grid.add_widget(stat_grid)
        self.statistic_grid.add_widget(antivirus_box)


class DevPanelItem(TabbedPanelItem):
    def __init__(self, icon_box, statistic_grid, **kwargs):
        super(DevPanelItem, self).__init__(**kwargs)
        self.icon_box = icon_box
        self.statistic_grid = statistic_grid

    def on_press(self):
        self.icon_box.clear_widgets()
        self.icon_box.add_widget(Image(source=config.data_center[self.text][0]))  # TODO: добавить анимацию перехода
        self.statistic_grid.clear_widgets()
        stat_grid = GridLayout(cols=1, size_hint_y=.4)
        stealth_label = Label(text=f"Знаний в час: 28")
        active_defence_label = Label(text=f"Текущий уровень: 3")
        stat_grid.add_widget(stealth_label)
        stat_grid.add_widget(active_defence_label)
        dev_box = BoxLayout(orientation='vertical', size_hint_y=.6)
        dev_label = Label(text='Разработка', size_hint_y=.2)
        dev_icon = Image(source=config.current_antivirus_tech[1], size_hint_y=.6)
        dev_progress = Label(text=config.current_antivirus_tech[2], size_hint_y=.2)
        dev_box.add_widget(dev_label)
        dev_box.add_widget(dev_icon)
        dev_box.add_widget(dev_progress)
        self.statistic_grid.add_widget(stat_grid)
        self.statistic_grid.add_widget(dev_box)


class UpgradePanelItem(TabbedPanelItem):
    def __init__(self, icon_box, statistic_grid, **kwargs):
        super(UpgradePanelItem, self).__init__(**kwargs)
        self.icon_box = icon_box
        self.statistic_grid = statistic_grid

    def on_press(self):
        self.icon_box.clear_widgets()
        self.icon_box.add_widget(Image(source=config.data_center[self.text][0]))  # TODO: добавить анимацию перехода
        self.statistic_grid.clear_widgets()

        # self.statistic_grid.add_widget()


class ProgramLayout(ButtonBehavior, BoxLayout):  # TODO: обновить on_release для открытия доп. информации
    def __init__(self, upper_lay, program, programs_grid, **kwargs):
        super(ProgramLayout, self).__init__(**kwargs)
        self.upper_lay = upper_lay
        self.program = program
        self.programs_grid = programs_grid
        self.active = False

    def on_release(self):
        '''
        upgrade_bottom_box = UpBoxLayout(orientation='horizontal')
        upgrade_bottom_layout = GridLayout(cols=1, size_hint_x=.8, pos_hint=({'center_x': .5}))
        upgrade_bottom_label = Label(text=str(self.upgrade_info[0]))
        upgrade_bottom_layout.add_widget(upgrade_bottom_label)
        for lay in self.upgrade_grid.lay_list:
            if lay.active:
                anim_height_down = HeightAnimation(lay, height=80, duration=.3)
                anim_height_down.start(lay.upper_lay)

        if not self.active:
            anim_height_up = Animation(height=200, duration=.6)
            anim_height_up.start(self.upper_lay)
            self.pos_hint = ({'top': 1})
            upgrade_bottom_box.add_widget(upgrade_bottom_layout)
            self.upper_lay.add_widget(upgrade_bottom_box)
            self.active = True
        '''
        pass


class ProgramGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(ProgramGridLayout, self).__init__(**kwargs)
        self.lay_list = None


class DevItemIcon(BoxLayout, ButtonBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.disabled:
            self.opacity = .5

    def on_release(self):
        pass


class ProgramsRelativeLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(ProgramsRelativeLayout, self).__init__(**kwargs)


class GifLineHorizontal(Image):
    def __init__(self, **kwargs):
        super(GifLineHorizontal, self).__init__(**kwargs)
        self.source = r'data/images/gui_elements/label.png'  # line.zip
        self.allow_stretch = True
        self.keep_ratio = False
        self.size_hint_y = None
        self.height = 1


class GifLineVertical(Image):
    def __init__(self, **kwargs):
        super(GifLineVertical, self).__init__(**kwargs)
        self.source = r'data/images/gui_elements/label.png'  # vline.zip
        self.allow_stretch = True
        self.keep_ratio = False
        self.size_hint_x = None
        self.width = 1


class DevScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(DevScrollView, self).__init__(**kwargs)


class InfoImage(ButtonBehavior, Image, HoverBehavior):
    def __init__(self, info, **kwargs):
        super(InfoImage, self).__init__(**kwargs)
        self.source = r'data/images/gui_elements/info.png'
        self.info = info

    def on_release(self):
        popup = Popup(title=str(self.info), size_hint=(.29, .5))
        popup.content = InfoLabel(text=config.descriptions[self.info], pos_hint=({'center_y': .5}))
        popup.open()

    def on_enter(self):
        self.source = r'data/images/gui_elements/info_hover.png'

    def on_leave(self):
        self.source = r'data/images/gui_elements/info.png'


class InfoLabel(Label):
    pass


class DefAmountLabel(Label):
    pass