import config
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


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
                if config.resources['Сырьевые ресурсы'][0] - res_cost[2][i] <= 0:
                    self.disabled = True
                    box_horizontal.opacity = .3
            else:
                if config.resources['Еда'][0] + res_cost[2][i] >= config.resources['Еда'][3] or \
                        config.resources['Электричество'][
                            0] + res_cost[2][i] >= config.resources['Электричество'][3]:
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
        i = 0
        for res in config.resources:
            if res == 'Сырьевые ресурсы':
                buildres = config.buildings[self.build_name][2]
                config.resources[res][0] -= buildres[i]
            else:
                buildres = config.buildings[self.build_name][2]
                config.resources[res][0] += buildres[i]
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


class MenuLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MenuLayout, self).__init__(**kwargs)
        self.size_hint = (.55, .7)
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


class FrameBoxLayout(BoxLayout):
    pass


class UpBoxLayout(BoxLayout):
    pass


class UpperBoxLayout(BoxLayout):
    pass


class IconImage(Image):
    pass


class BuildTimeLabel(Label):
    pass


class BuildingBoxLayout(BoxLayout):
    pass


class BuildResLabel(Label):
    pass


class BuildNameLabel(Label):
    pass


class BuildButton(Button):
    pass


class PlaceLabel(Label):
    pass
