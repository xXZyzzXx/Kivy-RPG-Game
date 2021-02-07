from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterPlaneLayout
from kivy.uix.screenmanager import Screen

from gui_list.iso import IsoFloatLayout, IsoHightLightImage, ChoiceHightligh, IsoTileImage, MovesHightlight, \
    IsoRightMenu, IsoNavMenu, IsoToggle, IsoCity, CityLabelName, CityViewButton, IsoMapUnit, ExpeditionButton
from tile_map import MyMap
import additional as ad
import config


class IsoMapScreen(Screen):  # Скрин карты
    def __init__(self, **kw):
        super(IsoMapScreen, self).__init__(**kw)
        self.hightlight = None
        self.map_scatter = None
        self.layout = None
        self.map_lay = None
        self.map = None
        self.choice_hl = None
        self.in_radius = False
        self.selected_moves_list = []
        self.group_menu = GroupMenu()

    def on_enter(self, *args):
        self.layout = RelativeLayout()
        self.map = MyMap(source="data/maps/first.tmx")  # Загруженная карта
        self.map_scatter = MyScatterLayout()  # Управление картой
        self.map_lay = IsoFloatLayout(mymap=self.map)  # Сама карта
        self.hightlight = IsoHightLightImage()  # Подсветка под мышкой
        config.hl = self.hightlight
        config.map_gui_list.insert(0, self.hightlight)
        self.choice_hl = ChoiceHightligh()  # Подсветка
        for layer in self.map.layers:  # Отрисовка тайлов карты
            for tile in layer:
                self.map_lay.add_widget(IsoTileImage(source=tile.image, pos=(tile.x, tile.y),
                                                     size=(tile.width, tile.height), size_hint=(None, None)))
                tile_info = Label(pos=(tile.x, tile.y), size=(tile.width, tile.height),
                                  text=f'{tile.column_index, tile.row_index}',
                                  size_hint=(None, None), color=(1, 1, 1, 1), font_size=12)  # \n{tile.x}, {tile.y}
                # self.map_lay.add_widget(tile_info)
        # self.map_lay.add_widget(self.hightlight)
        # self.map_lay.add_widget(self.choice_hl)
        config.city_list.clear()  # TODO: правильная отрисовка юнитов в зависимости от принадлежности
        for player in config.game.players:
            if player == config.current_player:
                for pre_city in player.pre_cities:
                    self.create_city(pre_city.pos, pre_city.name, player=player, owner=True)
                ad.change_current_city(player.cities[-1])  # Дефолтный город
            else:
                for pre_city in player.pre_cities:
                    self.create_city(pre_city.pos, pre_city.name, player=player)
                for unit in player.map_units:
                    self.map_lay.add_widget(unit)
        navigation = BoxLayout(orientation='vertical', size_hint=(.25, .05), pos_hint=({'center_x': .5, 'top': 1}))
        navigation.add_widget(Button(text='Переключить на город',
                                     on_press=lambda x: ad.set_screen('main', self.manager)))

        self.map_scatter.add_widget(self.map_lay)
        self.layout.add_widget(self.map_scatter)  # Игровая карта
        self.layout.add_widget(navigation)  # Панель навигации
        self.layout.add_widget(self.city_view())  # Переключения на города
        self.layout.add_widget(self.nav_right_content())
        self.layout.add_widget(self.expedition_content())
        self.add_widget(self.layout)
        Window.bind(mouse_pos=self.on_mouse_pos)
        ad.change_view(config.current_city, self.map_scatter, quick=True)

    def on_mouse_pos(self, window, pos):
        map_offset = self.map_scatter.pos
        cur_coords = (pos[0] - map_offset[0], pos[1] - map_offset[1])
        if cur_coords[0] > 0 and cur_coords[1] > 0:
            if ad.world_to_tile(cur_coords) is not None:
                current_coords = ad.world_to_tile(cur_coords)
                if self.hightlight.coordinates != current_coords:
                    self.in_radius = False  # убрать self?
                    self.get_highlight(current_coords)
                    if config.current_player.selected_unit is not None:  # хайлайт при выборе игрока
                        if config.current_player.selected_unit.selected:  # TODO: убрать двойное наложение
                            for moves in config.current_player.selected_unit.possible_moves:  # стоит ли делать цикл?
                                if current_coords == moves[-1][0]:
                                    self.get_road_to_tile(moves)
                                    self.in_radius = True
                            if not self.in_radius:
                                self.remove_selected_moves_list()  # убрать подсветку
                else:
                    if not self.hightlight.enter:
                        self.hightlight.opacity = 1
            else:
                self.hightlight.opacity = 0

    def get_road_to_tile(self, moves):
        self.remove_selected_moves_list()
        for move in moves:
            hl = MovesHightlight(pos=ad.tile_to_world(move[0]))
            self.map_lay.add_widget(hl)
            self.selected_moves_list.append(hl)

        ad.bring_to_front()

    def remove_selected_moves_list(self):
        for m in self.selected_moves_list:
            self.map_lay.remove_widget(m)

    def get_highlight(self, current_coords):
        if not self.hightlight.enter:
            self.hightlight.opacity = 1
        self.hightlight.pos = ad.tile_to_world(current_coords)
        # print(f'TILE: {current_coords}, pos: {self.hightlight.pos}')
        self.hightlight.coordinates = current_coords

    def build_group_menu(self):
        self.group_menu.build_base_ui()
        self.group_menu.build_ui()

    def expedition_content(self):
        main_lay = IsoNavMenu(orientation='horizontal', size_hint_y=None, height=30, pos_hint=({'bottom': 1}))
        # =============
        main_lay.add_widget(ExpeditionButton(pos_hint=({'left': 0}), size_hint_x=0.1,
                                             on_release=lambda x: self.open_expedition_menu()))
        return main_lay

    def open_expedition_menu(self):
        if self.group_menu.active:
            self.group_menu.clear_widgets()
            self.layout.remove_widget(self.group_menu)
            self.group_menu.active = False
        else:
            self.build_group_menu()
            self.layout.add_widget(self.group_menu)
            self.group_menu.active = True

    def nav_right_content(self):
        lay = IsoRightMenu(orientation='horizontal', size_hint=(.17, .5))
        main_lay = IsoNavMenu(orientation='vertical', size_hint_x=.9)
        toggle_button = IsoToggle(menu=lay, size_hint=(.1, .2), pos_hint=({'center_y': .5}))
        # =============
        main_lay.add_widget(Label(text='Управление экспедицией', size_hint_y=.1, font_size=16, pos_hint=({'top': 1})))
        unit_label = Label(text='Доступные юниты: ', size_hint=(.8, .7))
        main_lay.add_widget(unit_label)
        for unit in config.current_player.units:
            if config.current_player.units[unit] > 0:
                unit_label.text += f'\n{unit} {config.current_player.units[unit]}'
        main_lay.add_widget(Button(text='next turn', size_hint=(.8, .1), pos_hint=({'center_x': .5}),
                                   on_release=lambda x: self.refresh_movement()))
        main_lay.add_widget(Button(text='create', size_hint=(.8, .1), pos_hint=({'center_x': .5}),
                                   on_release=lambda x: self.create_expedition(config.current_city)))
        lay.add_widget(toggle_button)
        lay.add_widget(main_lay)
        toggle_button.menu_open()
        return lay

    @staticmethod
    def refresh_movement():
        for unit in config.current_player.map_units:
            unit.movement = unit.default_movement
            unit.move_points = unit.default_move_points
            unit.info_label.text = f'{unit.name} ({unit.default_move_points}/{unit.move_points})'
        if config.current_player.selected_unit is not None:
            config.current_player.selected_unit.clear_move_list()
            config.current_player.selected_unit.create_move_path()

    def on_leave(self, *args):
        self.clear_widgets()
        self.map_lay.clear_widgets()

    def create_city(self, pos, name, player, owner=False):
        city = IsoCity(pos=ad.tile_to_world(pos), coordinates=pos, hg=self.hightlight, name=name, player=player)
        city_info = CityLabelName(text=city.name, center_x=city.center_x, y=city.y + city.height * 0.8)
        config.map_gui_list.append(city)
        config.map_gui_list.append(city_info)
        if not owner:
            city_info.color = (1, 0, 0, 1)
        city.label = city_info
        player.cities.append(city)
        config.city_list.append(city)  # Для навигации
        self.map_lay.add_widget(city)
        self.map_lay.add_widget(city_info)
        self.map.city_list.append(city)

    def city_view(self):
        city_view = GridLayout(rows=1, size_hint=(.25, .05), pos_hint=({'top': 1}))
        for city in config.city_list:
            city_view.add_widget(CityViewButton(city=city, root=self.map_scatter))
        return city_view

    def create_expedition(self, city, unit='Воин'):  # TODO: reformat expedition for any units
        self.add_obj_to_map(unit, city.pos, city.coordinates)

    def add_obj_to_map(self, obj, pos, coords):  # Добавлять воина, а не объект
        unit = IsoMapUnit(name=obj, pos=pos, player=config.current_player, coords=coords, hl=self.choice_hl,
                          map=self.map)
        self.map_lay.add_widget(unit)
        config.current_player.map_units.append(unit)
        config.map_gui_list.append(unit)


# ====================================


class MyScatterLayout(ScatterPlaneLayout):
    def __init__(self, **kwargs):
        super(MyScatterLayout, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                self.zoom('down')
            elif touch.button == 'scrollup':
                self.zoom('up')
        ScatterPlaneLayout.on_touch_down(self, touch)

    def zoom(self, direction):  # TODO: доделать зум на карте
        if direction == 'down':
            self.scale += .1

        elif direction == 'up':
            self.scale -= .1

        # print(config.SCALING)


class GroupMenuBase(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (.9, .8)
        self.pos_hint = ({'center_x': .5, 'center_y': .5})
        self.active = False
        # =====

    def build_base_ui(self):
        self.top_box = BoxLayout(orientation='horizontal', size_hint_y=0.45)
        self.top_left_box = BoxLayout(orientation='horizontal', size_hint_x=0.2)
        self.top_center_box = BoxLayout(orientation='horizontal', size_hint_x=0.4)
        self.top_right_box = BoxLayout(orientation='horizontal', size_hint_x=0.2)
        self.top_box.add_widget(self.top_left_box)
        self.top_box.add_widget(self.top_center_box)
        self.top_box.add_widget(self.top_right_box)
        # ====
        self.bottom_box = BoxLayout(orientation='horizontal', size_hint_y=0.55)
        self.bottom_left_box = BoxLayout(orientation='horizontal', size_hint_x=0.2)
        self.bottom_center_box = BoxLayout(orientation='horizontal', size_hint_x=0.4)
        self.bottom_right_box = BoxLayout(orientation='horizontal', size_hint_x=0.2)
        self.bottom_box.add_widget(self.bottom_left_box)
        self.bottom_box.add_widget(self.bottom_center_box)
        self.bottom_box.add_widget(self.bottom_right_box)
        # ====
        self.add_widget(self.top_box)
        self.add_widget(self.bottom_box)


class GroupMenu(GroupMenuBase):
    def __init__(self, **kwargs):
        super(GroupMenu, self).__init__(**kwargs)
        # ====

    def build_ui(self):
        self.medical_box = GroupMainBox()
        self.character_box = GroupMainBox()
        self.specials_box = GroupMainBox()
        self.top_left_box.add_widget(self.medical_box)
        self.top_center_box.add_widget(self.character_box)
        self.top_right_box.add_widget(self.specials_box)
        # ====
        self.companions_box = GroupMainBox()
        self.inventory_box = GroupMainBox()
        self.specials_box = GroupMainBox()
        self.bottom_left_box.add_widget(self.companions_box)
        self.bottom_center_box.add_widget(self.inventory_box)
        self.bottom_right_box.add_widget(self.specials_box)
        # ====


class GroupMainBox(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.orientation = 'vertical'
        self.size_hint = (.9, .9)
        self.pos_hint = ({'center_x': .5, 'center_y': .5})
