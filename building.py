from gui import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader


def create_building_list(build_type, build_place, scatter):
    scroll = BuildingScrollView(do_scroll_x=False)  # , scroll_distance=200, scroll_timeout=5
    building_grid = GridLayout(cols=1, padding=5, spacing=5, size_hint_y=None)
    building_grid.bind(minimum_height=building_grid.setter('height'))
    for build_name in config.buildings:
        building = config.buildings[build_name]
        if build_type == 'Все':
            inside_building(building_grid, build_name, building, build_place, scatter)
        elif building[4] == build_type:
            inside_building(building_grid, build_name, building, build_place, scatter)
    scroll.add_widget(building_grid)
    return scroll


def inside_building(building_grid, build_name, building, build_place, scatter, *args):
    b_layout = BuildingBoxLayout(orientation='vertical', size_hint_y=None)
    box_horizontal = BoxLayout(orientation='horizontal')
    icon_layout = BoxLayout(orientation='vertical', size_hint_x=.2, padding=3)
    b_time_label = BuildTimeLabel(text=f'{building[1]} сек', size_hint_y=.2)
    b_icon = IconImage(source=f'{building[3]}', size_hint_y=.8)
    icon_layout.add_widget(b_time_label)
    icon_layout.add_widget(b_icon)
    res_layout = BoxLayout(orientation='horizontal')
    res_box_lay = ResLayout(build_type=building[4])
    test_lay = BoxLayout(size_hint=(1, .8), pos_hint=({'center_y': .5}), padding=15)
    for i, res_cost in enumerate(building[2]):
        if res_cost > 0:
            res_list = list(config.resources.keys())  # TODO:
            res_icon = Image(source=f'{config.resources[res_list[i]][2]}', size=(30, 30),
                             pos_hint=({'right': 1}),
                             size_hint=(None, 1))
            test = BuildResLabel(text=f'{res_cost}')
            res_box = BoxLayout(orientation='horizontal', size_hint_x=.5)
            help_lay_res = RelativeLayout()
            help_lay_res.add_widget(res_icon)
            add_lay = GridLayout(cols=2, size_hint=(1, 1), pos_hint=({'center_x': .5, 'center_y': .5}))
            add_lay.add_widget(help_lay_res)
            add_lay.add_widget(test)
            res_box.add_widget(add_lay)
            test_lay.add_widget(res_box)
    help_box = BoxLayout(size_hint_x=.1, padding=1)
    butt_lay = BuildingButt(build_name, build_place, scatter, box_horizontal)
    help_box.add_widget(butt_lay)
    res_box_lay.add_widget(test_lay)
    res_layout.add_widget(res_box_lay)
    res_layout.add_widget(help_box)
    box_horizontal.add_widget(icon_layout)
    box_horizontal.add_widget(res_layout)
    b_layout.add_widget(BuildNameLabel(text=f'{build_name}', size_hint_y=.3))
    b_layout.add_widget(box_horizontal)
    building_grid.add_widget(b_layout)


def menu_content(build_place):
    tb = TabbedPanel(do_default_tab=False, tab_width=150)
    tab_all = TabbedPanelHeader(text='Все')
    tab_war = TabbedPanelHeader(text='Военные')
    tab_prod = TabbedPanelItem(text='Производственные')
    tab_social = TabbedPanelHeader(text='Социальные')
    scatter = ScatterLayout(id='scatter_layout')  # size_hint_max=(1000, 800)
    name_label = PlaceLabel(text=f'Место для строительства: {build_place.id}')
    menu = MenuLayout()
    inside_menu = InsideMenuLayout()
    tb.add_widget(tab_all)
    tb.add_widget(tab_war)
    tb.add_widget(tab_social)
    tb.add_widget(tab_prod)
    for tab in tb.tab_list:
        tab.content = create_building_list(tab.text, build_place, scatter)
    inside_menu.add_widget(tb)
    menu.add_widget(inside_menu)
    menu.add_widget(name_label)
    close_b = CloseMenuButton(build_place, scatter)
    menu.add_widget(close_b)
    scatter.add_widget(menu)
    return scatter


def prod_upgrade_content():
    lay_list = []
    scroll = ScrollView()
    upgrade_grid = UpgradeGridLayout(cols=1, spacing=5, size_hint_y=None)
    upgrade_grid.bind(minimum_height=upgrade_grid.setter('height'))
    for upgrade_name in config.prod_upgrades:
        upgrade_info = config.prod_upgrades[upgrade_name]
        upper_lay = UpperBoxLayout(orientation='vertical', height=80, size_hint_y=None)
        top_box = TopUpgradeLayout(orientation='horizontal', height=80, size_hint_y=None, upper_lay=upper_lay,
                                   info=upgrade_info, upgrade_grid=upgrade_grid)
        lay_list.append(top_box)
        image_lay = BoxLayout(size_hint_x=.35)
        image_lay.add_widget(Image(source=upgrade_info[1]))
        title_box = BoxLayout(orientation='vertical', size_hint_x=.45)
        title_label = Label(text=f'{upgrade_name}')
        title_box.add_widget(title_label)
        upgrade_button = Button(text='Up', size_hint_x=.1)
        top_box.add_widget(image_lay)
        top_box.add_widget(title_box)
        top_box.add_widget(upgrade_button)
        upper_lay.add_widget(top_box)
        upgrade_grid.add_widget(upper_lay)

    upgrade_grid.lay_list = lay_list
    scroll.add_widget(upgrade_grid)
    return scroll


def prod_menu(build_place):
    scatter = ScatterLayout()
    menu = MenuLayout()
    inside_menu = InsideMenuLayout()
    main_box = BoxLayout(orientation='horizontal')
    left_box = BoxLayout(orientation='vertical', size_hint_x=.35)
    right_box = BoxLayout(size_hint_x=.65)
    icon_bottom_box = BoxLayout(size_hint=(.9, .8))
    icon_layout = BoxLayout(size_hint_y=.4)  # pos_hint=({'top': 1})
    statistic_grid = GridLayout(cols=1, size_hint_y=None, pos_hint=({'top': .9}), spacing=10, padding=5)
    for r in config.resources:
        res = config.resources[r]
        stat_box = BoxLayout(orientation='horizontal', height=40, size_hint_y=None)
        stat_box.add_widget(Image(source=res[2], size_hint_x=.2))
        stat_box.add_widget(Label(text=f'{res[0]}', size_hint_x=.8))
        statistic_grid.add_widget(stat_box)
    tb = TabbedPanel(do_default_tab=False, tab_width=130)
    ti = TabbedPanelItem(text='Улучшения')
    ti.content = prod_upgrade_content()
    tb.add_widget(ti)
    tb.add_widget(TabbedPanelItem(text='Автоматизация'))
    tb.add_widget(TabbedPanelItem(text='Статистика'))
    icon_bottom_box.add_widget(statistic_grid)
    icon_layout.add_widget(Image(source='data/images/buildings/buildings.zip'))
    left_box.add_widget(icon_layout)
    left_box.add_widget(icon_bottom_box)
    right_box.add_widget(tb)
    main_box.add_widget(left_box)
    main_box.add_widget(right_box)
    inside_menu.add_widget(main_box)
    close_b = CloseMenuButton(build_place, scatter)
    menu.add_widget(inside_menu)
    menu.add_widget(close_b)
    scatter.add_widget(menu)
    return scatter


def base_window(build_place):  # Шаблон для окна
    scatter = ScatterLayout()
    menu = MenuLayout()
    inside_menu = InsideMenuLayout()
    main_box = BoxLayout(orientation='horizontal', minimum_size=(700, 400))
    left_box = BoxLayout(orientation='vertical', size_hint_x=.3)
    right_box = BoxLayout(size_hint_x=.7)
    bottom_box = BoxLayout(size_hint=(.95, .8))
    icon_box = FrameBoxLayout(orientation='vertical', size_hint_y=.4)
    statistic_grid = GridLayout(cols=1, spacing=10, padding=5)
    icon_box.add_widget(Image(source=config.empty_icon))
    left_box.add_widget(icon_box)
    bottom_box.add_widget(statistic_grid)
    left_box.add_widget(bottom_box)
    main_box.add_widget(left_box)
    main_box.add_widget(right_box)
    inside_menu.add_widget(main_box)
    close_b = CloseMenuButton(build_place, scatter)
    menu.add_widget(inside_menu)
    menu.add_widget(close_b)
    scatter.add_widget(menu)
    return scatter, icon_box, statistic_grid, right_box






