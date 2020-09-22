from kivy.uix.floatlayout import FloatLayout
import config
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
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
            res_list = list(config.resourses.keys()) #TODO:
            res_icon = Image(source=f'{config.resourses[res_list[i]][2]}', size=(30, 30),
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
    for r in config.resourses:
        res = config.resourses[r]
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



def base_window(build_place):  # Шаблон
    scatter = ScatterLayout()
    menu = MenuLayout()
    inside_menu = InsideMenuLayout()
    main_box = BoxLayout(orientation='horizontal')
    left_box = BoxLayout(orientation='vertical', size_hint_x=.3)
    right_box = BoxLayout(size_hint_x=.7)
    bottom_box = BoxLayout(size_hint=(.9, .8))
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


class MenuLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MenuLayout, self).__init__(**kwargs)
        self.size_hint = (.6, .7)
        self.pos_hint = ({'center_x': .5, 'center_y': .5})


class InsideMenuLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(InsideMenuLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (.9, .87)
        self.pos_hint = ({'center_x': .5, 'center_y': .5})


class CloseMenuButton(ButtonBehavior, Image):
    def __init__(self, building, close_lay, **kwargs):
        super(CloseMenuButton, self).__init__(**kwargs)
        self.source = 'data/images/gui_elements/close.png'
        self.size = (20, 20)
        self.size_hint = (None, None)
        self.pos_hint = {"right": .98, "top": .98}
        self.close_lay = close_lay
        self.building = building

    def on_press(self):
        self.source = 'data/images/gui_elements/close.png'

    def on_release(self):  # Закрывает окно, сделать красивее
        self.source = 'data/images/gui_elements/close.png'
        self.building.parent.remove_widget(self.close_lay)
        self.building.active = False


class BuildingButt(ButtonBehavior, BoxLayout):
    def __init__(self, build_name, build_place, scatter, box_horizontal, **kwargs):
        super(BuildingButt, self).__init__(**kwargs)
        self.build_name = build_name
        self.build_place = build_place
        self.scatter = scatter
        with self.canvas.before:
            self.bg = Rectangle(pos=self.pos, size=self.size, source='data/images/gui_elements/build_button.png')
        res_cost = config.buildings[build_name]
        for i in range(3):
            if i == 2:
                if config.resourses['Сырьевые ресурсы'][0] - res_cost[2][i] <= 0:
                    self.disabled = True
                    box_horizontal.opacity=.3
            else:
                if config.resourses['Еда'][0] + res_cost[2][i] >= config.resourses['Еда'][3] or config.resourses['Электричество'][
                    0] + res_cost[2][i] >= config.resourses['Электричество'][3]:
                    self.disabled = True
                    box_horizontal.opacity = .3



    def on_size(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def on_press(self):
        pass

    def on_release(self):
        self.build_place.create_building(self.build_name)
        self.build_place.parent.remove_widget(self.scatter)
        i=0
        for res in config.resourses:
            if res=='Сырьевые ресурсы':
                buildres = config.buildings[self.build_name][2]
                config.resourses[res][0] -= buildres[i]
            else:
                buildres = config.buildings[self.build_name][2]
                config.resourses[res][0] += buildres[i]
                i += 1
        self.build_place.active = False


class ResLayout(BoxLayout):  # TODO: add color by building type
    def __init__(self, build_type, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (.6, 1)
        self.pos_hint = ({'center_y': .5})
        self.build_type = build_type
        color = config.type_colors[build_type]
        with self.canvas.before:
            Color(color[0], color[1], color[2], color[3], mode='rgba')
            self.bg = Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos


class BuildingScrollView(ScrollView):
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                pass
            elif touch.button == 'scrollup':
                if self.scroll_y < 0.17:
                    self.rel.add_widget(Button(text='suka'), pos_hint=({'top': .1}))
                print(self.scroll_y)
        return super(BuildingScrollView, self).on_touch_down(touch)'''
    pass


class TopUpgradeLayout(ButtonBehavior, BoxLayout):
    def __init__(self, upper_lay, info, upgrade_grid, **kwargs):
        super(TopUpgradeLayout, self).__init__(**kwargs)
        self.upper_lay = upper_lay
        self.upgrade_info = info
        self.upgrade_grid = upgrade_grid
        self.active = False

    def on_release(self):
        upgrade_bottom_box = UpBoxLayout(orientation='horizontal')
        upgrade_bottom_layout = GridLayout(cols=1, size_hint_x=.8, pos_hint=({'center_x': .5}))
        upgrade_bottom_label = Label(text=str(self.upgrade_info[0]))
        upgrade_bottom_layout.add_widget(upgrade_bottom_label)
        for lay in self.upgrade_grid.lay_list:
            if lay.active:
                anim_height_down = HeightAnimation(lay, height=80, duration=.2)
                anim_height_down.start(lay.upper_lay)

        if not self.active:
            anim_height_up = Animation(height=200, duration=.6)
            anim_height_up.start(self.upper_lay)
            self.pos_hint = ({'top': 1})
            upgrade_bottom_box.add_widget(upgrade_bottom_layout)
            self.upper_lay.add_widget(upgrade_bottom_box)
            self.active = True


class HeightAnimation(Animation):
    def __init__(self, lay, **kwargs):
        super(HeightAnimation, self).__init__(**kwargs)
        self.lay = lay

    def on_complete(self, widget):
        self.lay.upper_lay.remove_widget(self.lay.upper_lay.children[0])
        self.lay.active = False


class UpgradeGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(UpgradeGridLayout, self).__init__(**kwargs)
        self.lay_list = None


class FrameBoxLayout(BoxLayout):
    pass


class UpBoxLayout(BoxLayout):
    pass


class UpperBoxLayout(BoxLayout):
    pass


class PlaceLabel(Label):
    pass


class IconImage(Image):
    pass


class BuildTimeLabel(Label):
    pass


class BuildingBoxLayout(BoxLayout):
    pass


class BuildNameLabel(Label):
    pass


class BuildButton(Button):
    pass



class BuildResLabel(Label):
    pass