from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from functools import partial
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.uix.togglebutton import ToggleButton, ToggleButtonBehavior
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.properties import ListProperty, OptionProperty, StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.slider import Slider
from kivy.uix.image import Image, AsyncImage
from kivy.uix.checkbox import CheckBox
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelContent, TabbedPanelHeader
import config
import building
from data_center import DevScrollView, ProgramsRelativeLayout





def base_energy():
    scroll = DevScrollView(do_scroll_x=False, scroll_x=.5, scroll_y=1)
    main_rel_layout = RelativeLayout(height=500, width=600, size_hint=(1, 1))
    generators_lay = GridLayout(rows=2,padding=20)
    generators_desc = BoxLayout(size_hint_y=1)

    generators_stack = GridLayout(rows=1,size_hint=(1,0.5))

#generators stack content
    dev_item1 = BoxLayout(padding=5)
    dev_item2 = BoxLayout(padding=5)
    dev_item3 = BoxLayout(padding=5)
    dev_item4 = BoxLayout(padding=5)

    dev_item1.add_widget(GenImage())
    dev_item2.add_widget(GenImage())
    dev_item3.add_widget(GenImage())
    dev_item4.add_widget(GenImage())

    generators_stack.add_widget(dev_item1)
    generators_stack.add_widget(dev_item2)
    generators_stack.add_widget(dev_item3)
    generators_stack.add_widget(dev_item4)
# generators stack content

# generators description content
    generators_desc.add_widget(Label(text='Описание генераторов'))
# generators description content


    generators_lay.add_widget(generators_stack)
    generators_lay.add_widget(generators_desc)

    main_rel_layout.add_widget(generators_lay)

    scroll.add_widget(main_rel_layout)
    return scroll

def base_food():
    pass



def main_base_menu(build_place):
    scatter = ScatterLayout()
    menu = building.MenuLayout()
    inside_menu = building.InsideMenuLayout()
    main_box = BoxLayout(orientation='horizontal')
    left_box = BoxLayout(orientation='vertical', size_hint_x=.35)
    right_box = BoxLayout(size_hint_x=.65)
    icon_bottom_box = BoxLayout(size_hint=(.9, .8))
    icon_layout = BoxLayout(size_hint_y=.4)  # pos_hint=({'top': 1})

    # Вывод производства ресурсов
    stat_res=res_generation('main_base')

    #Добавление вкладок Здания
    tb = TabbedPanel(do_default_tab=False, tab_width=130)
    base_e = TabbedPanelItem(text='Энергия')
    base_e.content = base_energy()
    base_f = TabbedPanelItem(text='Пища')
    base_f.content = base_food()
    tb.add_widget(base_e)
    tb.add_widget(base_f)

    icon_bottom_box.add_widget(stat_res)
    icon_layout.add_widget(Image(source='data/images/buildings/main-base.png'))
    left_box.add_widget(icon_layout)
    left_box.add_widget(icon_bottom_box)
    right_box.add_widget(tb)
    main_box.add_widget(left_box)
    main_box.add_widget(right_box)
    inside_menu.add_widget(main_box)
    close_b = building.CloseMenuButton(build_place, scatter)
    menu.add_widget(inside_menu)
    menu.add_widget(close_b)
    scatter.add_widget(menu)
    return scatter

def res_generation(id_build):
    statistic_grid = GridLayout(cols=1, size_hint_y=None, pos_hint=({'top': .9}), spacing=10, padding=5)
    res_gen = BoxLayout(orientation='horizontal', height=40, size_hint_y=None)
    res_gen.add_widget(Label(text='Производит ресурсов', size_hint_x=.8))
    statistic_grid.add_widget(res_gen)
    for r in config.resourses:
        res = config.resourses[r]
        build_name = config.resourses_generation[id_build]
        if build_name[r] > 0:
            stat_box = BoxLayout(orientation='horizontal', height=40, size_hint_y=None)
            stat_box.add_widget(Image(source=res[2], size_hint_x=.2))
            stat_box.add_widget(Label(text=f'{build_name[r]}', size_hint_x=.8))
            statistic_grid.add_widget(stat_box)
    return statistic_grid

class GenImage(BoxLayout, ButtonBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.disabled:
            self.opacity = .2

    def gen_set(self):
        scatter = ScatterLayout()
        menu = building.MenuLayout()
        inside_menu = building.InsideMenuLayout()
        main_box = BoxLayout(orientation='horizontal')
        left_box = BoxLayout(orientation='vertical', size_hint_x=.35)
        right_box = BoxLayout(size_hint_x=.65)
        icon_bottom_box = BoxLayout(size_hint=(.9, .8))
        icon_layout = BoxLayout(size_hint_y=.4)  # pos_hint=({'top': 1})
        left_box.add_widget(icon_layout)
        left_box.add_widget(icon_bottom_box)
        main_box.add_widget(left_box)
        main_box.add_widget(right_box)
        inside_menu.add_widget(main_box)
        close_b = building.CloseMenuButton(self, scatter)
        menu.add_widget(inside_menu)
        menu.add_widget(close_b)
        scatter.add_widget(menu)
        return scatter

    