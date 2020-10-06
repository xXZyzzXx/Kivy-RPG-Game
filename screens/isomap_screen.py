import config
import additional as ad
from gui import *
from kivy.core.window import Window
from kivy.uix.scatterlayout import ScatterPlaneLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen


def set_screen(name_screen, sm):
    sm.current = name_screen


class IsoMapScreen(Screen):
    def __init__(self, **kw):
        super(IsoMapScreen, self).__init__(**kw)
        self.hightlight = None
        self.map_scatter = None
        self.layout = None
        self.map_lay = None
        self.map = None

    def on_mouse_pos(self, window, pos):
        map_offset = self.map_scatter.pos
        cur_coords = (pos[0] - map_offset[0], pos[1] - map_offset[1])
        if cur_coords[0] > 0 and cur_coords[1] > 0:
            if ad.world_to_tile(cur_coords) is not None:
                current_coords = ad.world_to_tile(cur_coords)
                # print(current_coords)
                if self.hightlight.coordinates != current_coords:
                    self.get_highlight(current_coords)
                else:
                    if not self.hightlight.enter:
                        self.hightlight.opacity = 1
            else:
                self.hightlight.opacity = 0

    def get_highlight(self, current_coords):
        if not self.hightlight.enter:
            self.hightlight.opacity = 1
        self.hightlight.pos = ad.tile_to_world(current_coords)
        # print(f'TILE: {current_coords}, pos: {self.hightlight.pos}')
        self.hightlight.coordinates = current_coords

    def on_enter(self, *args):
        from tile_map import MyMap, Tile
        self.layout = RelativeLayout()
        self.map = MyMap()
        self.map_scatter = MyScatterLayout()
        self.map_lay = IsoFloatLayout(map=self.map)
        self.hightlight = IsoHightLightImage()
        for layer in self.map.layers:
            for tile in layer:
                self.map_lay.add_widget(IsoTileImage(source=tile.image, pos=(tile.x, tile.y),
                                                     size=(tile.width, tile.height), size_hint=(None, None)))
                tile_info = Label(pos=(tile.x, tile.y), size=(tile.width, tile.height),
                                  text=f'{tile.column_index, tile.row_index}\n{tile.x}, {tile.y}',
                                  size_hint=(None, None), color=(1, 1, 1, 1), font_size=12)
                # self.map_lay.add_widget(tile_info)
        self.create_city((2, 46), name='Персеполис')
        self.create_city((3, 41), name='Научград')
        navigation = BoxLayout(orientation='vertical', size_hint=(.2, .02), pos_hint=({'center_x': .5, 'top': 1}))
        navigation.add_widget(Button(text='Переключить на город',
                                     on_press=lambda x: set_screen('main', self.manager)))
        self.map_lay.add_widget(self.hightlight)
        self.map_scatter.add_widget(self.map_lay)
        self.layout.add_widget(self.map_scatter)
        self.layout.add_widget(navigation)
        self.add_widget(self.layout)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_leave(self, *args):
        self.clear_widgets()

    def create_city(self, pos, name):
        city = City(pos=ad.tile_to_world(pos), coordinates=pos, hg=self.hightlight, name=name)
        city_info = CityLabelName(text=city.name, center_x=city.center_x, y=city.y + city.height * 0.8)
        city.label = city_info
        self.map_lay.add_widget(city)
        self.map_lay.add_widget(city_info)
        self.map.city_list.append(city)


class MyScatterLayout(ScatterPlaneLayout):  # MAIN LAYOUT in ISO
    def __init__(self, **kwargs):
        super(MyScatterLayout, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                self.zoom('down')
            elif touch.button == 'scrollup':
                self.zoom('up')
        ScatterPlaneLayout.on_touch_down(self, touch)

    def zoom(self, direction):
        if direction == 'down':
            config.SCALING += .1
            self.scale = config.SCALING
        elif direction == 'up':
            config.SCALING -= .1
            self.scale = config.SCALING
        print(config.SCALING)