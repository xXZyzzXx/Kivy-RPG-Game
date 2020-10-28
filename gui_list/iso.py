import additional as ad
import config
import libraries.a_star as pathfind
from additional import HoverBehavior
from kivy.animation import Animation
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget


class IsoTileImage(Widget):
    def __init__(self, source, pos, size, **kwargs):
        super(IsoTileImage, self).__init__(**kwargs)
        with self.canvas:
            self.image = Rectangle(source=source, pos=pos, size=size)

    def on_size(self, *args):
        self.image.size = self.size
        self.image.pos = self.pos


class IsoHightLightImage(Image):
    def __init__(self, **kwargs):
        super(IsoHightLightImage, self).__init__(**kwargs)
        self.source = r'data/images/iso/hightlight.png'
        self.enter = False
        self.opacity = 0
        self.size = (config.TILE_WIDTH * config.SCALING, config.TILE_HEIGHT * config.SCALING + 10 * config.SCALING)
        self.size_hint = (None, None)
        self.coordinates = None


class IsoFloatLayout(FloatLayout):
    def __init__(self, mymap, **kwargs):
        super(IsoFloatLayout, self).__init__(**kwargs)
        self.moved = False
        self.map = mymap
        self.in_radius = False

    def on_touch_down(self, touch):
        touch.grab(self)
        return super(IsoFloatLayout, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.moved:
            self.moved = True
        if touch.grab_current is self:
            root_pos = self.parent.pos
            if int(root_pos[0]) < 0:
                pass
        else:
            pass
        return super(IsoFloatLayout, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if touch.button == 'left':
                if not self.moved:
                    tiles = ad.world_to_tile(touch.pos)
                    if tiles is not None:
                        self.check_press(tiles)
                    if config.current_player.selected_unit is not None:
                        self.in_radius = False
                        if config.current_player.selected_unit.selected:  # Снятие выделения
                            for moves in config.current_player.selected_unit.possible_moves:
                                if tiles == moves[-1][0]:
                                    for i, move in enumerate(moves):
                                        if i == 0:
                                            continue
                                        else:
                                            anim = Animation(pos=ad.tile_to_world_adv(move[0]), duration=.7)
                                            anim.start(config.current_player.selected_unit)
                                            config.current_player.selected_unit.movement -= move[1]
                                            config.current_player.selected_unit.move_points -= 1
                                            config.current_player.selected_unit.info_label.text = f'{config.current_player.selected_unit.name} ({config.current_player.selected_unit.default_move_points}/{config.current_player.selected_unit.move_points})'
                                    config.hl.opacity = 0
                                    config.current_player.selected_unit.coords = moves[-1][0]
                                    self.parent.parent.parent.remove_selected_moves_list()
                                    self.in_radius = True
                                    if config.current_player.selected_unit.movement > 10:
                                        if tiles != moves[0][0]:
                                            config.current_player.selected_unit.create_move_path()
                                    else:
                                        self.remove_movement()
                            if not self.in_radius:
                                self.remove_movement()

                else:
                    self.moved = False
        else:
            pass
        return super(IsoFloatLayout, self).on_touch_up(touch)

    def remove_movement(self):
        config.current_player.selected_unit.selected = False
        config.current_player.selected_unit = None
        self.remove_units_moves()

    def remove_units_moves(self):
        for unit in config.current_player.map_units:
            unit.clear_move_list()

    def check_press(self, tiles):
        flag = False  # Для выхода из двух циклов
        flag2 = False
        for lay in self.map.layers:
            for tile in lay:
                for unit in config.current_player.map_units:
                    if unit.coords == tiles:
                        unit.create_move_path()
                        flag = True
                        flag2 = True
                        break
                if flag2:
                    break
                if tile.coordinates == tiles:
                    if tile.type == 'city':
                        if not tile.tools:
                            self.remove_info()
                            tile.get_panel()
                    else:
                        self.remove_info()
                        print(f'Выбранный тайл: {tiles}')
                    flag = True
                    break
            if flag:
                break

    def remove_info(self):  # TODO: при удалении двери пропадает hightlight opacity
        for city in self.map.city_list:
            if city.player == config.current_player:
                door = city.door_tool
                expedition = city.expedition_tool
                if door is not None:
                    anim_top = DownDoorAnim(y=city.top - city.height / 3, x=city.x + city.width / 3, opacity=.75,
                                            parent=self,
                                            door=door, width=door.width / 2, height=door.height / 1.5, duration=.3)
                    anim_expedition = DownDoorAnim(y=city.top - city.height / 3, x=city.x + city.width / 2, opacity=0,
                                                   parent=self,
                                                   door=expedition, width=expedition.width / 2,
                                                   height=expedition.height / 2, duration=.3)
                    anim_top.start(door)
                    anim_expedition.start(expedition)
                    if door in config.map_gui_list and expedition in config.map_gui_list:
                        config.map_gui_list.remove(door)
                        config.map_gui_list.remove(expedition)
            else:
                attack = city.attack_tool
                hack = city.hack_tool
                if attack is not None and hack is not None:
                    anim_left = DownDoorAnim(y=city.top - city.height / 3, x=city.x + city.width / 3, opacity=0,
                                             parent=self,
                                             door=attack, width=attack.width / 2, height=attack.height / 2, duration=.3)
                    anim_right = DownDoorAnim(y=city.top - city.height / 3, x=city.x + city.width / 2, opacity=0,
                                              parent=self,
                                              door=hack, width=hack.width / 2, height=hack.height / 2, duration=.3)
                    anim_left.start(city.attack_tool)
                    anim_right.start(city.hack_tool)
                    if attack in config.map_gui_list and hack in config.map_gui_list:
                        config.map_gui_list.remove(attack)
                        config.map_gui_list.remove(hack)
            city.tools = False


class CityViewButton(Button):
    def __init__(self, city, root, **kwargs):
        super(CityViewButton, self).__init__(**kwargs)
        self.city = city
        self.root_scatter = root
        self.text = city.name

    def on_release(self):
        ad.change_view(self.city, self.root_scatter)


class IsoRelativeLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(IsoRelativeLayout, self).__init__(**kwargs)


class IsoCity(Image):
    def __init__(self, pos, coordinates, hg, player, name='default', **kwargs):
        super(IsoCity, self).__init__(**kwargs)
        self.size = (config.TILE_WIDTH * config.SCALING, config.TILE_HEIGHT * config.SCALING)
        self.source = r"data/images/buildings/barracks.png"
        self.pos = (pos[0], pos[1] + 10 * config.SCALING)
        self.hightlight = hg
        self.coordinates = coordinates
        self.size_hint = (None, None)
        self.type = 'city'
        self.label = None
        self.door_tool = None
        self.attack_tool = None
        self.hack_tool = None
        self.expedition_tool = None
        self.tools = False
        self.name = name
        self.player = player

    def get_panel(self):
        if self.player == config.current_player:
            door = CityToolButton(source=r'data/images/iso/doors.png', city=self, hl=self.hightlight, name='door')
            expedition = CityToolButton(source=r'data/images/iso/expedition.png', city=self, hl=self.hightlight,
                                        name='expedition')
            top_anim = Animation(x=door.x - door.width / 2 - 3, y=door.y + door.default_pos, opacity=1, duration=.3)
            expedition_anim = Animation(x=expedition.x + expedition.width / 2 + 3, y=door.y + expedition.default_pos,
                                        opacity=1, duration=.3)
            self.door_tool = door
            self.expedition_tool = expedition
            self.parent.add_widget(door)
            self.parent.add_widget(expedition)
            top_anim.start(door)
            expedition_anim.start(expedition)
            config.map_gui_list.append(door)
            config.map_gui_list.append(expedition)
        else:
            attack = CityToolButton(source=r'data/images/iso/attack.png', city=self, hl=self.hightlight, name='attack')
            hack = CityToolButton(source=r'data/images/iso/hack.png', city=self, hl=self.hightlight, name='hack')
            left_anim = Animation(y=attack.y + attack.default_pos, x=attack.x - attack.width / 2 - 3, opacity=1,
                                  duration=.3)
            right_anim = Animation(y=hack.y + hack.default_pos, x=hack.x + hack.width / 2 + 3, opacity=1, duration=.3)
            self.attack_tool = attack
            self.hack_tool = hack
            self.parent.add_widget(hack)
            self.parent.add_widget(attack)
            left_anim.start(attack)
            right_anim.start(hack)
            config.map_gui_list.append(attack)
            config.map_gui_list.append(hack)

        self.label.bring_to_front()
        self.tools = True


class CityToolButton(ButtonBehavior, HoverBehavior, Image):
    def __init__(self, source, city, hl, name, df=40, **kwargs):
        super(CityToolButton, self).__init__(**kwargs)
        self.source = source
        self.width = (config.TILE_WIDTH * config.SCALING) / 2.4
        self.height = self.width
        self.opacity = .9
        self.city = city
        self.name = name
        self.default_pos = df
        self.pos = (city.pos[0] + (city.width - self.width) / 2, city.top - city.height / 3)
        self.size_hint = (None, None)
        self.hightlight = hl

    def on_release(self):
        if self.name == 'door':
            app = App.get_running_app()
            app.root.current = 'main'
        elif self.name == 'expedition':
            print('expedition')

    def on_enter(self):
        if self.name == 'door':
            self.source = r'data/images/iso/doors_hover.png'
        self.hightlight.enter = True
        self.hightlight.opacity = 0

    def on_leave(self):
        if self.name == 'door':
            self.source = r'data/images/iso/doors.png'
        self.hightlight.enter = False
        self.hightlight.opacity = 1


class DownDoorAnim(Animation):
    def __init__(self, parent, door, **kwargs):
        super(DownDoorAnim, self).__init__(**kwargs)
        self.parent = parent
        self.door = door

    def on_complete(self, widget):
        self.parent.remove_widget(self.door)


class CityLabelName(Label):
    def __init__(self, color=(1, 1, 0, 1), **kwargs):
        super(CityLabelName, self).__init__(**kwargs)
        self.color = color
        self.size_hint = (None, None)
        self.size = (220 * config.SCALING, 60 * config.SCALING)

    def bring_to_front(self):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(self)


class IsoToggle(ButtonBehavior, Image):
    def __init__(self, menu, **kwargs):
        super(IsoToggle, self).__init__(**kwargs)
        self.toggle_state = True
        self.source = r'data/images/iso/arrows_back.png'
        self.keep_ratio = False
        self.allow_stretch = True
        self.menu = menu

    def on_release(self):
        if self.toggle_state:
            self.menu_close()
        else:
            self.menu_open()

    def menu_close(self):
        self.source = r'data/images/iso/arrows.png'
        self.toggle_state = False
        anim = Animation(x_hint=1.153, duration=.3)
        anim.start(self.menu)

    def menu_open(self):
        self.source = r'data/images/iso/arrows_back.png'
        self.toggle_state = True
        anim = Animation(x_hint=1, duration=.3)
        anim.start(self.menu)


class IsoMapUnit(ButtonBehavior, BoxLayout):
    def __init__(self, name, coords, player, hl=None, map=None, **kwargs):
        super(IsoMapUnit, self).__init__(**kwargs)
        self.source = r'data/images/Units/warrior.png'
        self.orientation = 'vertical'
        self.hl = hl  # Подсветка
        self.coords = coords
        self.map = map
        self.size_hint = (None, None)
        self.width = config.TILE_WIDTH * config.SCALING
        self.height = config.TILE_HEIGHT * config.SCALING + 10
        self.name = name
        self.default_movement = 30
        self.default_move_points = 2
        self.move_points = self.default_move_points
        self.movement = self.default_movement
        self.moves_highlight_list = []
        self.selected = False
        self.possible_moves = []
        self.player = player
        unit_label_color = (.7, 0, 0, 1)
        unit_label_text = f'{name}'
        if player == config.current_player:
            unit_label_text = f'{name} ({self.default_move_points}/{self.move_points})'
            unit_label_color = (0, 0, 0, 1)
        self.info_label = Label(text=unit_label_text, size_hint_y=None, height=10, font_size=14, color=unit_label_color)
        self.add_widget(self.info_label)
        self.add_widget(Image(source=self.source, size_hint=(None, None), width=config.TILE_WIDTH * config.SCALING,
                              height=config.TILE_HEIGHT * config.SCALING))

    def on_release(self):
        # self.create_move_path()
        pass

    def create_move_path(self):
        self.clear_move_list()
        move_map = pathfind.create_move_map(int(self.coords[0]), int(self.coords[1]), self.movement, self.map)
        for move in move_map:
            disallow_highlight = False
            friendly_object = True
            for tile in self.map.objects_list:
                if move[-1][0] == tile.coordinates:
                    disallow_highlight = True
                    break
            if disallow_highlight:
                continue
            for city in self.map.city_list:
                if move[-1][0] == city.coordinates:
                    if city.player == config.current_player:
                        hl = EnterBuildingHightligh(pos=ad.tile_to_world(move[-1][0]))
                    else:
                        hl = EnemyBuildingHightligh(pos=ad.tile_to_world(move[-1][0]))
                    friendly_object = False
                    break
            for player in config.game.players:
                if player != config.current_player:
                    for unit in player.map_units:
                        if move[-1][0] == unit.coords:
                            hl = EnemyBuildingHightligh(pos=ad.tile_to_world(move[-1][0]))
                            friendly_object = False
            self.possible_moves.append(move)
            if move[-1][0] == self.coords:
                continue
            if friendly_object:
                hl = ChoiceHightligh(pos=ad.tile_to_world(move[-1][0]))
            anim = Animation(opacity=1, duration=.2)
            anim.start(hl)
            self.parent.add_widget(hl)
            self.moves_highlight_list.append(hl)
        ad.bring_to_front()
        config.current_player.selected_unit = self
        self.selected = True
        for unit in config.current_player.map_units:
            if unit == self:
                continue
            else:
                unit.clear_move_list()

    def clear_move_list(self):
        for item in self.moves_highlight_list:
            anim = RemoveMovesAnimation(opacity=0, duration=.3, parent=self.parent, widget=item)
            anim.start(item)
        self.moves_highlight_list.clear()
        self.possible_moves.clear()


class ChoiceHightligh(Image):
    def __init__(self, opacity=0.2, **kwargs):
        super(ChoiceHightligh, self).__init__(**kwargs)
        self.source = r'data/images/iso/hightlight5.png'
        self.choice = None
        self.opacity = opacity
        self.size = (config.TILE_WIDTH * config.SCALING, config.TILE_HEIGHT * config.SCALING + 10 * config.SCALING)
        self.size_hint = (None, None)
        self.coordinates = None


class EnterBuildingHightligh(Image):
    def __init__(self, opacity=0.2, **kwargs):
        super(EnterBuildingHightligh, self).__init__(**kwargs)
        self.source = r'data/images/iso/player_building_highlight.png'
        self.choice = None
        self.opacity = opacity
        self.size = (config.TILE_WIDTH * config.SCALING, config.TILE_HEIGHT * config.SCALING + 10 * config.SCALING)
        self.size_hint = (None, None)
        self.coordinates = None


class EnemyBuildingHightligh(Image):
    def __init__(self, opacity=0.2, **kwargs):
        super(EnemyBuildingHightligh, self).__init__(**kwargs)
        self.source = r'data/images/iso/enemy_hightlight.png'
        self.choice = None
        self.opacity = opacity
        self.size = (config.TILE_WIDTH * config.SCALING, config.TILE_HEIGHT * config.SCALING + 10 * config.SCALING)
        self.size_hint = (None, None)
        self.coordinates = None


class MovesHightlight(Image):
    def __init__(self, opacity=1, **kwargs):
        super(MovesHightlight, self).__init__(**kwargs)
        self.source = r'data/images/iso/hightlight.png'
        self.choice = None
        self.opacity = opacity
        self.size = (config.TILE_WIDTH * config.SCALING, config.TILE_HEIGHT * config.SCALING + 10 * config.SCALING)
        self.size_hint = (None, None)
        self.coordinates = None


class IsoRightMenu(BoxLayout):
    pass


class IsoNavMenu(BoxLayout):
    pass


class RemoveMovesAnimation(Animation):
    def __init__(self, parent, widget, **kwargs):
        super(RemoveMovesAnimation, self).__init__(**kwargs)
        self.parent = parent
        self.widget = widget

    def on_complete(self, widget):
        self.parent.remove_widget(self.widget)


class UnitLabel(Label):
    pass