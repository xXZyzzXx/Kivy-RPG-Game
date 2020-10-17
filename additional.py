from kivy.core.window import Window
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.properties import BooleanProperty, ObjectProperty
import config


class HoverBehavior(object):
    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """

    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        # Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            # We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass


Factory.register('HoverBehavior', HoverBehavior)


def subregion(px, py, r_x, r_y):
    rx = int(r_x)
    ry = int(r_y)
    foo = px - py
    bar = px + py
    # print(f'{px - py:.3f}, {px + py:.3f} | {px, py} | {foo, bar}')
    if foo < 0 and bar > 1:  # Top
        return rx, ry
    elif foo < 0 and bar < 1:  # Left
        if r_y > 0:
            if py > 0.5:
                return rx - 1, ry + 1
            return rx - 1, ry
        else:
            return None
    elif foo > 0 and bar > 1:  # Right
        if r_y > 0:
            if py > 0.5:
                return rx, ry + 1
            return rx, ry
        else:
            return None
    elif foo > 0 and bar < 1:  # Bottom
        if r_y < 0 or py == 0:
            return rx, ry
        return rx, ry + 1


def world_to_tile(pos):  # TODO: добавить правильный зум
    TILE_WIDTH = config.TILE_WIDTH
    TILE_HEIGHT = config.TILE_HEIGHT
    mw = config.MW
    mh = config.MH
    x, y = pos
    y -= 10 * config.SCALING  # height of a tile
    r_x = x / (TILE_WIDTH * config.SCALING)
    r_y = mh - (y / (TILE_HEIGHT * config.SCALING)) * 2
    if r_x >= 0 and r_y >= -1:
        MouseMapX = x % (TILE_WIDTH * config.SCALING)
        MouseMapY = y % (TILE_HEIGHT * config.SCALING)
        map_x = MouseMapX / (TILE_WIDTH * config.SCALING)
        map_y = MouseMapY / (TILE_HEIGHT * config.SCALING)
        result = subregion(map_x, map_y, r_x, r_y)
        if result is not None:
            if -1 < result[0] < mw and -1 < result[1] < mh:
                return result


def tile_to_world(pos):
    column_index, row_index = pos
    if row_index % 2 == 0:
        x = column_index * (config.TILE_WIDTH * config.SCALING)
        y = (config.MH - row_index - 1) * ((config.TILE_HEIGHT * config.SCALING) / 2)
    else:
        x = column_index * (config.TILE_WIDTH * config.SCALING) + ((config.TILE_WIDTH * config.SCALING) / 2)
        y = (config.MH - row_index - 1) * ((config.TILE_HEIGHT * config.SCALING) / 2)
    # print(x, y)
    return x, y


def set_screen(name_screen, sm):
    sm.current = name_screen


def change_view(obj, root, quick=False):
    if quick:
        root.pos = -(obj.pos[0] - Window.width / 2 + obj.width / 2), -(obj.pos[1] - Window.height / 2 + obj.height / 2)
    else:
        anim = Animation(
            pos=(-(obj.pos[0] - Window.width / 2 + obj.width / 2), -(obj.pos[1] - Window.height / 2 + obj.height / 2)),
            duration=.5)
        anim.start(root)


def change_current_city(city):
    config.current_city = city
