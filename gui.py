import re

import building
import config
from additional import *
from building import *
from kivy.animation import Animation
from kivy.graphics import Rectangle
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
from kivy.uix.textinput import TextInput

res_list = list(config.resourses.keys())
anim_opacity_up = Animation(opacity=1, duration=.5)
anim_opacity_down = Animation(opacity=0, duration=.5)


def on_checkbox_active(checkbox, value):
    if value:
        checkbox.slider.disabled = False
        checkbox.txt_inp.disabled = False
        checkbox.h_button.disabled = False
        anim = Animation(my_x_hint=.5, duration=.5)
        for b in checkbox.bl:
            b.disabled = False
            b.opacity = 1
            anim.start(b)
        how_many = checkbox.available_label
        checkbox.slider.current_unit = checkbox.unit
        checkbox.slider.max = int(how_many.text)
        checkbox.slider.total_inside.unit = checkbox.unit
        checkbox.slider.available_label = checkbox.available_label
        checkbox.h_button.unit = checkbox.unit
        checkbox.slider.allow_total_res = True
        checkbox.slider.total_inside.count_total()
    else:
        allow_disabled = True  # Check if all checkbox is unactive
        for item in checkbox.slider.group_list:
            if item.active:
                allow_disabled = False
                break
        # === Start =======================
        if allow_disabled:
            checkbox.slider.disabled = True
            checkbox.txt_inp.disabled = True
            checkbox.h_button.disabled = True
            anim = Animation(my_x_hint=1, opacity=0, duration=.5)
            for b in checkbox.bl:
                b.disabled = True
                anim.start(b)


class MoneyImage(Image):
    def __init__(self, **kwargs):
        super(MoneyImage, self).__init__(**kwargs)


class MapButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MapButton, self).__init__(**kwargs)
        self.source = 'data/images/navigation/map.png'


class WarButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(WarButton, self).__init__(**kwargs)
        self.source = 'data/images/navigation/attack.png'


class ReportButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ReportButton, self).__init__(**kwargs)
        self.source = 'data/images/navigation/pechat.png'


class MailButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MailButton, self).__init__(**kwargs)
        self.source = 'data/images/navigation/letter.png'

#Инициализация базы
class BuildingBase(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(BuildingBase, self).__init__(**kwargs)
        self.source = 'data/images/buildings/main-base.png'
        self.free_space = False
        self.active = False
        self.name = 'main_base'
        self.unit_grid = None
        self.slider = None
        self.available_list = None

    def on_release(self):
        self.parent.add_widget(building.main_base_menu(build_place=self))



class Building(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Building, self).__init__(**kwargs)
        self.source = 'data/images/city/empty_place.png'
        self.free_space = True
        self.active = False
        self.name = 'Foundament'
        self.unit_grid = None
        self.slider = None
        self.available_list = None

    def create_building(self, build_name):
        path_to_building = config.buildings[build_name][3]
        self.source = path_to_building
        self.name = build_name
        self.free_space = False

    def on_press(self):
        pass

    def on_release(self):
        if self.free_space:
            self.parent.add_widget(building.menu_content(build_place=self))
        else:
            self.parent.add_widget(self.building_content(build_place=self, build=self.name))
            self.active = True

    def update_available_units(self):  # , grid, slider
        final = []  # TODO: Remove it, need to add ZeroDevision except
        for unit in config.buildings[self.name][5]:  # Для каждого юнита
            li = []
            for i, res in enumerate(config.units[unit][2]):
                if res > 0:
                    res_cost = config.resourses[res_list[i]][0]
                    li.append(res_cost / res)
            how_many_unit = int(min(li))
            final.append(how_many_unit)
        if len(self.available_list) > 0:
            for j, widget in enumerate(self.available_list):
                widget.text = str(final[j])  # TODO: не работает как нужно
        if self.slider.available_label is not None:
            self.slider.max = int(self.slider.available_label.text)
        return final

    def building_content(self, build_place, build):
        building = config.buildings[build]
        scatter = ScatterLayout(id='town_hall_scatter')
        name_label = PlaceLabel(text=f'{build}, id: {build_place.id}')
        menu = MenuLayout()
        inside_menu = InsideMenuLayout()
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=.3)
        bottom_layout = BoxLayout(orientation='vertical', size_hint_y=.3)
        right_layout = BoxLayout(orientation='vertical')
        upgrade_layout = BoxLayout(orientation='horizontal', size_hint_y=.3)
        description_layout = BoxLayout(size_hint_y=.7)
        description_label = Label(text='Описание здания')
        description_layout.add_widget(description_label)
        icon_rel = BoxLayout(size_hint_x=.3)
        icon = Image(source=building[3])
        icon_rel.add_widget(icon)
        upgrade_label = Label(text=f'{building[1]} сек', size_hint_x=.9)
        upgrade_res_layout = BoxLayout(orientation='horizontal')
        for i, res_cost in enumerate(building[2]):
            if res_cost > 0:
                res_box = BoxLayout(orientation='horizontal', size_hint_x=.5)
                help_lay_res = RelativeLayout()
                help_lay_res.add_widget(Image(source=f'{config.resourses[res_list[i]][2]}', size=(25, 25),
                                              pos_hint=({'right': 1}), size_hint=(None, 1)))
                add_lay = GridLayout(cols=2, size_hint=(1, 1), pos_hint=({'center_x': .5, 'center_y': .5}))
                add_lay.add_widget(help_lay_res)
                add_lay.add_widget(BuildResLabel(text=f'{res_cost}'))
                res_box.add_widget(add_lay)
                upgrade_res_layout.add_widget(res_box)
        upgrade_button = Button(text='Up', size_hint_x=.1)
        upgrade_layout.add_widget(upgrade_button)
        upgrade_layout.add_widget(upgrade_label)
        upgrade_layout.add_widget(upgrade_res_layout)
        right_layout.add_widget(upgrade_layout)
        right_layout.add_widget(description_layout)
        top_layout.add_widget(icon_rel)
        top_layout.add_widget(right_layout)
        middle_lay = BoxLayout(size_hint_y=.4)
        slider_layout = BoxLayout(orientation='vertical', size_hint_y=.7)
        input_layout = BoxLayout(orientation='horizontal', size_hint=(.3, 1), pos_hint=({'right': 1}))
        text_input = UnitTextInput(text='0', size_hint_y=.9, pos_hint=({'center_y': .5}), multiline=False)
        total_res_layout = BoxLayout(orientation='horizontal', size_hint_x=.65, padding=5)
        self.slider = UnitSlider(text_input, size_hint_y=.55, padding=10)
        total_inside = TotalInsideLayout(orientation='horizontal', slider=self.slider)
        time_label = TotalTimeLabel(size_hint_y=.3, halign='left')
        total_res_label = TotalResLabel(text='Стоимость:', size_hint_x=.35)
        text_input.slider = self.slider
        self.slider.total_inside = total_inside
        self.slider.time_label = time_label
        self.slider.total_res_label = total_res_label
        hire_button = HireUnitsButton(text='Нанять', disabled=True, slider=self.slider, build_root=self)
        count_box = BoxLayout(orientation='vertical', size_hint_x=.25, padding=1, spacing=1)
        up_button = UpButton(opacity=0, slider=self.slider)
        down_button = DownButton(opacity=0, slider=self.slider)
        bottom_slider_lay = BoxLayout(orientation='horizontal', size_hint_y=.45)
        scroll_unit = ScrollView(do_scroll_x=False, scroll_distance=50, size_hint_y=.8, pos_hint=({'center_y': .5}))
        butt_list = [up_button, down_button]
        self.unit_grid = GridLayout(cols=1, padding=5, spacing=5, size_hint_y=None, opacity=0)
        self.unit_grid.bind(minimum_height=self.unit_grid.setter('height'))
        self.available_list = []
        checkbox_group_list = []

        for unit_name in building[5]:
            unit = config.units[unit_name]
            checkbox = UnitCheckBox(group='units', size_hint_x=.05, slider=self.slider, txt_inp=text_input,
                                    unit=unit_name, hb=hire_button, bl=butt_list, trl=total_res_label, tl=time_label)
            checkbox.bind(active=on_checkbox_active)
            checkbox_group_list.append(checkbox)
            grid_layout = UnitGridLayout(cols=6, size_hint_y=None, height=40, checkbox=checkbox)
            unit_icon = Image(source=unit[3], size_hint_x=.05)
            unit_name_label = Label(text=f'{unit_name}', size_hint_x=.2)
            unit_cost = BoxLayout(orientation='horizontal', size_hint_x=.45)
            for i, res_cost in enumerate(unit[2]):
                if res_cost > 0:
                    res_box = BoxLayout(orientation='horizontal', size_hint_x=.5)
                    help_lay_res = RelativeLayout()
                    help_lay_res.add_widget(Image(source=f'{config.resourses[res_list[i]][2]}', size=(25, 25),
                                                  pos_hint=({'right': 1}), size_hint=(None, 1)))
                    add_lay = GridLayout(cols=2, size_hint=(1, 1), pos_hint=({'center_x': .5, 'center_y': .5}))
                    add_lay.add_widget(help_lay_res)
                    add_lay.add_widget(BuildResLabel(text=f'{res_cost}'))
                    res_box.add_widget(add_lay)
                    unit_cost.add_widget(res_box)
            unit_time = Label(text=f'{unit[1]} сек', size_hint_x=.15)
            how_many_lay = BoxLayout(orientation='horizontal', size_hint_x=.1)
            available_label = Label(text='8', size_hint_y=.8, pos_hint=({'center_y': .5}))
            checkbox.available_label = available_label
            self.available_list.append(available_label)
            all_button = AllUnitButton(text='All', size_hint_y=.6, pos_hint=({'center_y': .5}), checkbox=checkbox)
            how_many_lay.add_widget(all_button)
            how_many_lay.add_widget(available_label)
            grid_layout.add_widget(checkbox)
            grid_layout.add_widget(unit_icon)
            grid_layout.add_widget(unit_name_label)
            grid_layout.add_widget(unit_cost)
            grid_layout.add_widget(unit_time)
            grid_layout.add_widget(how_many_lay)
            self.unit_grid.add_widget(grid_layout)

        self.slider.group_list = checkbox_group_list
        scroll_unit.add_widget(self.unit_grid)
        count_box.add_widget(up_button)
        count_box.add_widget(down_button)
        input_layout.add_widget(count_box)
        input_layout.add_widget(text_input)
        input_layout.add_widget(hire_button)
        slider_layout.add_widget(self.slider)
        total_res_layout.add_widget(total_res_label)
        total_res_layout.add_widget(total_inside)
        bottom_slider_lay.add_widget(total_res_layout)
        bottom_slider_lay.add_widget(input_layout)
        slider_layout.add_widget(bottom_slider_lay)
        middle_lay.add_widget(scroll_unit)
        bottom_layout.add_widget(slider_layout)
        bottom_layout.add_widget(time_label)
        inside_menu.add_widget(top_layout)
        inside_menu.add_widget(middle_lay)
        inside_menu.add_widget(bottom_layout)
        menu.add_widget(inside_menu)
        menu.add_widget(name_label)
        close_b = CloseMenuButton(self, scatter)
        menu.add_widget(close_b)
        scatter.add_widget(menu)
        self.update_available_units()
        anim_opacity_up.start(self.unit_grid)
        return scatter


class RockLayout(FloatLayout, HoverBehavior):  # BoxLayout
    def __init__(self, widget, **kwargs):
        super().__init__(**kwargs)
        self.widget = widget
        self.widget.size_hint = (.75, .75)
        self.widget.pos_hint = ({'center_x': .5, 'center_y': .52})
        self.add_widget(self.widget)
        with self.canvas.before:
            self.bg = Rectangle(pos=self.pos, size=self.size, source='data/images/gui_elements/rock_label.png')

    def on_size(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def on_enter(self, *args):
        # print("You are in, through this point", self.border_point)
        self.widget.size_hint = (.8, .8)
        self.widget.pos_hint = ({'center_x': .5, 'center_y': .55})
        self.canvas.before.clear()
        with self.canvas.before:
            self.bg = Rectangle(pos=self.pos, size=self.size, source='data/images/gui_elements/rock_label_hover.png')

    def on_leave(self, *args):
        # print("You left through this point", self.border_point)
        self.widget.size_hint = (.75, .75)
        self.widget.pos_hint = ({'center_x': .5, 'center_y': .52})
        self.canvas.before.clear()
        with self.canvas.before:
            self.bg = Rectangle(pos=self.pos, size=self.size, source='data/images/gui_elements/rock_label.png')


class UnitCheckBox(CheckBox):
    def __init__(self, slider, txt_inp, unit, hb, bl, trl, tl, **kwargs):
        super(UnitCheckBox, self).__init__(**kwargs)
        self.slider = slider
        self.available_label = 0
        self.h_button = hb  # Hire button (buy units)
        self.bl = bl  # buttlist(up and down buttons)
        self.total_res_label = trl
        self.time_label = tl
        self.txt_inp = txt_inp
        self.unit = unit

    def on_release(self):
        self.slider.value = 0
        self.txt_inp.text = '0'


class UnitGridLayout(ButtonBehavior, GridLayout):
    def __init__(self, checkbox, **kwargs):
        super(UnitGridLayout, self).__init__(**kwargs)
        self.checkbox = checkbox

    def on_release(self):
        self.checkbox.active = True
        self.checkbox.slider.value = 0
        self.checkbox.txt_inp.text = '0'


class AllUnitButton(Button):
    def __init__(self, checkbox, **kwargs):
        super(AllUnitButton, self).__init__(**kwargs)
        self.checkbox = checkbox

    def on_release(self):
        self.checkbox.active = True
        value = int(self.checkbox.available_label.text)
        self.checkbox.slider.max = value
        self.checkbox.slider.value = value
        self.checkbox.txt_inp.text = str(value)
        self.checkbox.slider.total_inside.count_total()


class UnitTextInput(TextInput, HoverBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.slider = None
        self.disabled = True
        self.bind(text=self.on_text_txt_inp, focus=self.on_focus_txt_inp)

    def on_enter(self, *args):
        pass  # print('here')

    def on_leave(self, *args):
        pass  # print('here')

    def on_text_txt_inp(self, instance, value):
        self.slider.total_inside.count_total()
        if value != '':
            if instance.slider.max >= int(value):
                instance.slider.value = value
            else:
                instance.slider.value = instance.slider.max
                instance.value = instance.slider.value
                instance.text = str(instance.slider.value)

    def on_focus_txt_inp(self, instance, value):
        if value:
            pass
        else:
            pass

    def insert_text(self, substring, from_undo=False):
        pat = re.compile('[^0-9]')
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(UnitTextInput, self).insert_text(s, from_undo=from_undo)


class UnitSlider(Slider):
    def __init__(self, text_input, **kwargs):
        super(UnitSlider, self).__init__(**kwargs)
        self.value_track = True
        self.value_track_color = get_color_from_hex('#75bbfd')
        self.cursor_size = (20, 20)
        self.min = 0
        self.max = 0
        self.step = 1
        self.disabled = True
        # =======================
        self.allow_total_res = False
        self.text_input = text_input
        self.total_res_label = None
        self.total_inside = None
        self.time_label = None
        self.available_label = None
        self.current_unit = None
        self.not_moved = True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            self.not_moved = False
            self.value_pos = touch.pos
            self.text_input.text = f'{int(self.value)}'
            return True

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.value_pos = touch.pos
            if self.allow_total_res:
                self.change_opacity()
            return True

    def change_opacity(self):
        anim_opacity_change_start = BlinkAnimation(opacity=.75, duration=.2, total_inside=self.total_inside,
                                                   txt_inp=self.text_input, slider_value=self.value)
        anim_opacity_change_start.start(self.total_inside)


class TotalInsideLayout(BoxLayout):
    def __init__(self, slider, **kwargs):
        super(TotalInsideLayout, self).__init__(**kwargs)
        self.slider = slider
        self.opacity = 0

    def count_total(self):
        self.clear_widgets()
        unit = config.units[self.slider.current_unit]
        time_to = '21:50:58'  # TODO: Temporary var, change to real time
        if self.slider.value > 0:
            total_time = unit[1] * int(self.slider.value)
            self.slider.time_label.text = f'Обучение продлится: {total_time} сек до {time_to}'
            for i, res_cost in enumerate(unit[2]):
                total_res = res_cost * int(self.slider.value)
                if res_cost > 0:
                    res_box = BoxLayout(orientation='horizontal', size_hint_x=.5)
                    help_lay_res = RelativeLayout()
                    help_lay_res.add_widget(Image(source=f'{config.resourses[res_list[i]][2]}', size=(30, 30),
                                                  pos_hint=({'right': 1}), size_hint=(None, 1)))
                    add_lay = GridLayout(cols=2, size_hint=(1, 1), pos_hint=({'center_x': .5, 'center_y': .5}))
                    add_lay.add_widget(help_lay_res)
                    add_lay.add_widget(BuildResLabel(text=f'{total_res}'))
                    res_box.add_widget(add_lay)
                    self.add_widget(res_box)
            anim_opacity_up.start(self)
            anim_opacity_up.start(self.slider.total_res_label)
            anim_opacity_up.start(self.slider.time_label)
        else:
            anim_opacity_down.start(self)
            anim_opacity_down.start(self.slider.total_res_label)
            anim_opacity_down.start(self.slider.time_label)


class HireUnitsButton(Button):
    def __init__(self, slider, build_root, **kwargs):
        super(HireUnitsButton, self).__init__(**kwargs)
        self.slider = slider
        self.build_root = build_root

    def on_release(self):
        self.buy_units()

    def buy_units(self):
        allow_buy = True
        for i, unit_cost in enumerate(config.units[self.unit][2]):  # Проверка можно ли купить
            res_cost = unit_cost * self.slider.value
            if res_cost > 0:
                if config.resourses[res_list[i]][0] < res_cost:
                    print(f'Недостаточно ресурсов: {config.resourses[res_list[i]][0]}, {res_cost}')
                    allow_buy = False
                    break
        if allow_buy:
            for i, unit_cost in enumerate(config.units[self.unit][2]):  # Проверка можно ли купить
                res_cost = unit_cost * self.slider.value
                if res_cost > 0:
                    if config.resourses[res_list[i]][0] >= res_cost:
                        config.resourses[res_list[i]][0] -= res_cost
            config.player_units[self.unit] += int(self.slider.value)
            self.build_root.update_available_units()
            curr_value = int(self.slider.available_label.text)
            self.slider.max = curr_value  # TODO: сделать корректное отображение
            if self.slider.value >= self.slider.max:
                self.slider.value = curr_value
                self.slider.text_input.text = str(curr_value)
            print(config.player_units)


class UpButton(ButtonBehavior, Image):
    def __init__(self, slider, **kwargs):
        super(UpButton, self).__init__(**kwargs)
        self.source = 'data/images/gui_elements/up_button.png'
        self.disabled = True
        self.slider = slider

    def on_release(self):
        if int(self.slider.value) < int(self.slider.max):
            self.slider.value += 1
            self.slider.text_input.text = f'{int(self.slider.text_input.text) + 1}'
            self.slider.total_inside.count_total()


class DownButton(ButtonBehavior, Image):
    def __init__(self, slider, **kwargs):
        super(DownButton, self).__init__(**kwargs)
        self.source = 'data/images/gui_elements/down_button.png'
        self.disabled = True
        self.slider = slider

    def on_release(self):
        if int(self.slider.value) or int(self.slider.text_input.text) > 0:
            self.slider.value -= 1
            self.slider.text_input.text = f'{int(self.slider.text_input.text) - 1}'
            self.slider.total_inside.count_total()


class BlinkAnimation(Animation):
    def __init__(self, total_inside, txt_inp, slider_value, **kwargs):
        super(BlinkAnimation, self).__init__(**kwargs)
        self.total_inside = total_inside
        self.text_input = txt_inp
        self.slider_value = slider_value

    def on_complete(self, widget):
        if widget is not None:
            self.text_input.text = f'{int(self.slider_value)}'
            anim_opacity_change_end = Animation(opacity=1, duration=.5)
            anim_opacity_change_end.start(self.total_inside)


class TestBoxLayout(BoxLayout):
    pass


class CityCanvas(RelativeLayout):
    pass


class RightSidebar(BoxLayout):
    pass


class SkladLabel(Label):
    pass


class ResLabel(Label):
    pass


class SidebarRes(BoxLayout):
    pass


class TotalTimeLabel(Label):
    pass


class TotalResLabel(Label):
    pass


class TerminalRelativeLayout(RelativeLayout):
    pass


class TerminalGridLayout(GridLayout):
    pass


class TerminalClose(ButtonBehavior, Image, HoverBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'data/images/gui_elements/terminal_close_normal.png'

    def on_enter(self):
        self.source = 'data/images/gui_elements/terminal_close_hovered.png'

    def on_leave(self):
        self.source = 'data/images/gui_elements/terminal_close_normal.png'

    def on_press(self):
        self.source = 'data/images/gui_elements/terminal_close_pressed.png'

    def on_release(self):
        self.source = 'data/images/gui_elements/terminal_close_hovered.png'


class TerminalIcon(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'data/images/gui_elements/terminal_icon.png'


class TerminalTitleLabel(Label):
    pass


class TerminalLabel(Label):
    pass


class TerminalScrollView(ScrollView):
    pass


class TerminalTextInput(TextInput):
    def __init__(self, grid, **kwargs):
        super(TerminalTextInput, self).__init__(**kwargs)
        self.grid = grid
        self.start_text = 'C:\JARVIS\Terminal>'
        self.text = self.start_text

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'enter':
            if self.text[:19] == 'C:\JARVIS\Terminal>':
                self.grid.remove_widget(self)
                self.grid.add_widget(TerminalLabel(text=self.start_text + self.text[19:]))
                self.grid.add_widget(TerminalTextInput(grid=self.grid, text=self.start_text))
            else:
                self.text = self.start_text