import config
import additional as ad
from additional import HoverBehavior
from kivy.animation import Animation
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout


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

    def on_touch_down(self, touch):
        touch.grab(self)

    def on_touch_move(self, touch):
        if not self.moved:
            self.moved = True
        if touch.grab_current is self:
            root_pos = self.parent.pos
            # print(f'Touch: {self}')
            # print(root_pos)
            if int(root_pos[0]) < 0:
                pass
        else:
            pass
            # it's a normal touch

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # I receive my grabbed touch, I must ungrab it!
            touch.ungrab(self)
            if touch.button == 'left':
                if not self.moved:
                    tiles = ad.world_to_tile(touch.pos)
                    if tiles is not None:
                        self.check_press(tiles)
                else:
                    self.moved = False
        else:
            # it's a normal touch
            pass

    def check_press(self, tiles):
        layers = [self.map.city_list, self.map.items_list, self.map.floor_list]
        flag = False  # Для выхода из двух циклов
        for lay in layers:
            for tile in lay:
                if tile.coordinates == tiles:
                    if tile.type == 'city':
                        print(tile)
                        if not tile.tools:
                            self.remove_info()
                            tile.get_panel()
                    else:
                        self.remove_info()
                        print(tiles)
                    flag = True
                    break
            if flag:
                break

    def remove_info(self):  # TODO: при удалении двери пропадает hightlight opacity
        for city in self.map.city_list:
            if city.player == config.current_player:
                door = city.door_tool
                if door is not None:
                    anim_top = DownDoorAnim(y=city.top - city.height / 3, x=door.x + door.width / 4, opacity=.75,
                                            parent=self,
                                            door=door, width=door.width / 2, height=door.height / 1.5, duration=.3)
                    anim_top.start(city.door_tool)
            else:
                attack = city.attack_tool
                hack = city.hack_tool
                if attack is not None and hack is not None:
                    anim_left = DownDoorAnim(y=city.top - city.height / 3, x=city.x + city.width/3, opacity=0,
                                             parent=self,
                                             door=attack, width=attack.width / 2, height=attack.height / 2, duration=.3)
                    anim_right = DownDoorAnim(y=city.top - city.height / 3, x=city.x + city.width / 2, opacity=0,
                                              parent=self,
                                              door=hack, width=hack.width / 2, height=hack.height / 2, duration=.3)
                    anim_left.start(city.attack_tool)
                    anim_right.start(city.hack_tool)
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
        self.tools = False
        self.name = name
        self.player = player

    def get_panel(self):
        if self.player == config.current_player:
            door = CityToolButton(source=r'data/images/iso/doors.png', city=self, hl=self.hightlight, name='door')
            top_anim = Animation(y=door.y + door.default_pos, opacity=1, duration=.3)
            self.door_tool = door
            self.parent.add_widget(door)
            top_anim.start(door)
        else:
            attack = CityToolButton(source=r'data/images/iso/attack.png', city=self, hl=self.hightlight, name='attack')
            hack = CityToolButton(source=r'data/images/iso/hack.png', city=self, hl=self.hightlight, name='hack')
            left_anim = Animation(y=attack.y + attack.default_pos, x=attack.x - attack.width/2 - 3, opacity=1,
                                  duration=.3)
            right_anim = Animation(y=hack.y + hack.default_pos, x=hack.x + hack.width/2 + 3, opacity=1, duration=.3)
            self.attack_tool = attack
            self.hack_tool = hack
            self.parent.add_widget(hack)
            self.parent.add_widget(attack)
            left_anim.start(attack)
            right_anim.start(hack)

        self.label.bring_to_front()
        self.tools = True


class CityToolButton(Image, HoverBehavior):
    def __init__(self, source, city, hl, name, df=40, **kwargs):
        super().__init__(**kwargs)
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
