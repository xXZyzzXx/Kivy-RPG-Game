from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.screenmanager import ShaderTransition
from kivy.animation import Animation
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
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


class PixelTransition(ShaderTransition):

    PIXEL_TRANSITION_FS = '''$HEADER$
        uniform float t;
        uniform sampler2D tex_in;
        uniform sampler2D tex_out;

        vec2 myround(vec2 x) {
            return vec2(floor(x.x + .5), floor(x.y + .5));
        }

        void main (void) {
            float pixels;
            float t2;
            if (t < 0.5)
                t2 = 1.0 - t * 2.0;
            else
                t2 = (t - 0.5) * 2.0;

            pixels = 5.0 + 1000.0 * t2 * t2;
            vec2 new = myround(tex_coord0.st * vec2(pixels,pixels)) /
                               vec2(pixels,pixels);

            vec4 c1 = vec4(texture2D(tex_out, new));
            vec4 c2 = vec4(texture2D(tex_in, tex_coord0.st));

            float a = min(1.0, max(0.0, (t - 0.4) / 0.2));

            gl_FragColor = c1 + vec4(a,a,a,a)*(c2-c1);
        }
    '''
    fs = StringProperty(PIXEL_TRANSITION_FS)


class RippleTransition(ShaderTransition):

    RIPPLE_TRANSITION_FS = '''$HEADER$
        uniform float t;
        uniform sampler2D tex_in;
        uniform sampler2D tex_out;

        void main (void) {
            float frequency = 20.0;
            float speed = 10.0;
            float amplitude = 0.05;
            vec2 center = vec2(0.5,0.5);
            vec2 toUV = tex_coord0.st - center;
            float distanceFromCenter = length(toUV);
            vec2 normToUV = toUV / distanceFromCenter;

            float wave = cos(frequency * distanceFromCenter - speed * t);
            float offset1 = t * wave * amplitude;
            float offset2 = (1.0 - t) * wave * amplitude;

            vec2 newUV1 = center + normToUV * vec2(distanceFromCenter+offset1,
                          distanceFromCenter + offset1);
            vec2 newUV2 = center + normToUV * vec2(distanceFromCenter+offset2,
                          distanceFromCenter + offset2);

            vec4 c1 =  vec4(texture2D(tex_out, newUV1));
            vec4 c2 =  vec4(texture2D(tex_in, newUV2));

            gl_FragColor = c1 + vec4(t,t,t,t)*(c2 - c1);
        }
    '''
    fs = StringProperty(RIPPLE_TRANSITION_FS)


class BlurTransition(ShaderTransition):

    BLUR_TRANSITION_FS = '''$HEADER$
        uniform float t;
        uniform sampler2D tex_in;
        uniform sampler2D tex_out;

        void main (void) {
            vec2 center = vec2(0.5,0.5);
            vec2 toUV = tex_coord0.st - center;

            vec4 c1 = vec4(0,0,0,0);
            int count = 24;
            float s = t * 0.02;

            for(int i=0; i<count; i++)
                c1 += texture2D(
                    tex_out,
                    tex_coord0.st - toUV * vec2(s,s) * vec2(i,i)
                );

            c1 /= vec4(count,count,count,count);
            vec4 c2 = vec4(texture2D(tex_in, tex_coord0.st));

            gl_FragColor = c1 + t*(c2 - c1);
        }
    '''
    fs = StringProperty(BLUR_TRANSITION_FS)


class RVBTransition(ShaderTransition):

    RVB_TRANSITION_FS = '''$HEADER$
        uniform float t;
        uniform sampler2D tex_in;
        uniform sampler2D tex_out;

        uniform vec2 resolution;

        void main(void)
        {
            vec2 uv = vec2(gl_FragCoord.x / resolution.x, gl_FragCoord.y /
                           resolution.y);

            float amount = 0.0;

            amount = (1.0 + sin(t*6.0)) * 0.5;
            amount *= 1.0 + sin(t*16.0) * 0.5;
            amount *= 1.0 + sin(t*19.0) * 0.5;
            amount *= 1.0 + sin(t*27.0) * 0.5;
            amount = pow(amount, 3.0);

            amount *= 0.03;

            vec3 col;
            col.r = texture2D( tex_out, vec2(uv.x+amount,uv.y) ).r * (1.0-t)
                  + texture2D( tex_in, vec2(uv.x+amount,uv.y) ).r  * t;
            col.g = texture2D( tex_out, uv ).g * (1.0-t)
                  + texture2D( tex_in, uv ).g * t;
            col.b = texture2D( tex_out, vec2(uv.x-amount,uv.y) ).b * (1.0-t)
                  + texture2D( tex_in, vec2(uv.x-amount,uv.y) ).b * t;

            col = vec3(col.r*(1.0 - amount * 0.5),
                       col.g*(1.0 - amount * 0.5),
                       col.b*(1.0 - amount * 0.5));

            gl_FragColor = vec4(col.r,col.g,col.b,1.0);
        }

    '''
    fs = StringProperty(RVB_TRANSITION_FS)

    def on_progress(self, progress):
        self.render_ctx['resolution'] = [float(wh) for wh in self.screen_out.size]
        super(RVBTransition, self).on_progress(progress)


class RotateTransition(ShaderTransition):
    '''Rotate transition.
    '''

    direction = OptionProperty('left', options=('left', 'right', 'up', 'down'))
    '''Direction of the transition.

    :data:`direction` is an :class:`~kivy.properties.OptionProperty`, default
    to left. Can be one of 'left', 'right', 'up' or 'down'.
    '''

    ROTATE_TRANSITION_HEADER = '''
        $HEADER$
        uniform float t;
        uniform sampler2D tex_in;
        uniform sampler2D tex_out;
        const vec4 shadow = vec4(0.0, 0.0, 0.0, 1.0);
        const float shadow_pow = 0.5;

        void main(void) {
    '''

    ROTATE_TRANSITION_FOOTER = '''
        vec4 cnew = cout;
        float light = pow(1.0-tt, shadow_pow);
        if ( tt + pos > 1.0) {
            cnew = cin;
            light=pow(tt, shadow_pow);
        }
        gl_FragColor = cnew*light*frag_color;
    }'''

    ROTATE_TRANSITION_LEFT = ROTATE_TRANSITION_HEADER + '''
        float tt = t;
        float pos = tex_coord0.x;
        vec4 cin = texture2D(tex_in,
                             vec2(1.0-(1.0-tex_coord0.x)/tt, tex_coord0.y));
        vec4 cout = texture2D(tex_out,
                              vec2(tex_coord0.x/(1.0-tt), tex_coord0.y));
    ''' + ROTATE_TRANSITION_FOOTER

    ROTATE_TRANSITION_RIGHT = ROTATE_TRANSITION_HEADER + '''
        float tt = 1.0 - t;
        float pos = tex_coord0.x;
        vec4 cin = texture2D(tex_out,
                             vec2(1.0-(1.0-tex_coord0.x)/tt, tex_coord0.y));
        vec4 cout = texture2D(tex_in,
                              vec2(tex_coord0.x/(1.0-tt), tex_coord0.y));
    ''' + ROTATE_TRANSITION_FOOTER

    ROTATE_TRANSITION_UP = ROTATE_TRANSITION_HEADER + '''
        float tt = t;
        float pos = tex_coord0.y;
        vec4 cin = texture2D(tex_in,
                             vec2(tex_coord0.x, 1.0-(1.0-tex_coord0.y)/tt));
        vec4 cout = texture2D(tex_out,
                              vec2(tex_coord0.x, tex_coord0.y/(1.0-tt)));
    ''' + ROTATE_TRANSITION_FOOTER

    ROTATE_TRANSITION_DOWN = ROTATE_TRANSITION_HEADER + '''
        float tt = 1.0 - t;
        float pos = tex_coord0.y;
        vec4 cin = texture2D(tex_out,
                             vec2(tex_coord0.x, 1.0-(1.0-tex_coord0.y)/tt));
        vec4 cout = texture2D(tex_in,
                              vec2(tex_coord0.x, tex_coord0.y/(1.0-tt)));
    ''' + ROTATE_TRANSITION_FOOTER

    fs = StringProperty(ROTATE_TRANSITION_LEFT)

    def __init__(self, **kwargs):
        self.on_direction(kwargs.get('direction', 'left'))
        super(RotateTransition, self).__init__(**kwargs)

    def on_direction(self, *largs):
        if largs[0] == 'left':
            self.fs = self.ROTATE_TRANSITION_LEFT
        if largs[0] == 'right':
            self.fs = self.ROTATE_TRANSITION_RIGHT
        if largs[0] == 'up':
            self.fs = self.ROTATE_TRANSITION_UP
        if largs[0] == 'down':
            self.fs = self.ROTATE_TRANSITION_DOWN


class FastSlideTransition(ShaderTransition):
    direction = OptionProperty('left', options=('left', 'right', 'up', 'down'))
    '''Direction of the transition.

    :data:`direction` is an :class:`~kivy.properties.OptionProperty`, default
    to left. Can be one of 'left', 'right', 'up' or 'down'.
    '''

    FAST_SLIDE_TRANSITION_UP = '''
    $HEADER$
    uniform float t;
    uniform sampler2D tex_in;
    uniform sampler2D tex_out;

    uniform vec2 resolution;

    float y2, n;
    float BLURMAX = 50.;
    float T = smoothstep(0., 1., t);
    void main(void){
        vec4 c = vec4(0., 0., 0., 0.);
        if (tex_coord0.y < 1. - T) {
            float squash = mix(.95, 1., pow(1. - t, 2.));
            float x = .5 + (tex_coord0.x - .5) / squash;
            float y = tex_coord0.y + T;

            if (0. < x && x < 1.) {
                for (n=0.; n < BLURMAX; n+=1.) {
                    y2 = y - n / resolution.y;
                    if (0. <= y2 && y2 <= 1.)
                        c += texture2D(tex_out, vec2(x, y2)) / BLURMAX;
                }
                gl_FragColor = mix(c, texture2D(tex_out, vec2(x, y)), pow(1. - t, 5.));
            } else
                gl_FragColor = vec4(0, 0, 0, 0);
        } else {
            float squash = mix(.95, 1., pow(t, 2.));
            float x = .5 + (tex_coord0.x - .5) / squash;
            float y = tex_coord0.y - 1. + T;

            if (0. < x && x < 1.) {
                for (n=0.; n < BLURMAX; n+=1.) {
                    y2 = y - n / resolution.y;
                    if (0. < y2 && y2 < 1.)
                        c += texture2D(tex_in, vec2(x, y2)) / BLURMAX;
                }
                gl_FragColor = mix(c, texture2D(tex_in, vec2(x, y)), pow(t, 5.));
            } else
                gl_FragColor = vec4(0, 0, 0, 0);
        }
    }
    '''  # noqa

    FAST_SLIDE_TRANSITION_LEFT = '''
    $HEADER$
    uniform float t;
    uniform sampler2D tex_in;
    uniform sampler2D tex_out;

    uniform vec2 resolution;

    float x2, n;
    float BLURMAX = 50.;
    float T = smoothstep(0., 1., t);
    void main(void){
        vec4 c = vec4(0., 0., 0., 0.);
        if (tex_coord0.x < 1. - T) {
            float squash = mix(.95, 1., pow(1. - t, 2.));
            float y = .5 + (tex_coord0.y - .5) / squash;
            float x = tex_coord0.x + T;

            if (0. < y && y < 1.) {
                for (n=0.; n < BLURMAX; n+=1.) {
                    x2 = x - n / resolution.x;
                    if (0. <= x2 && x2 <= 1.)
                        c += texture2D(tex_out, vec2(x2, y)) / BLURMAX;
                }
                gl_FragColor = mix(c, texture2D(tex_out, vec2(x, y)), pow(1. - t, 5.));
            } else
                gl_FragColor = vec4(0, 0, 0, 0);
        } else {
            float squash = mix(.95, 1., pow(t, 2.));
            float y = .5 + (tex_coord0.y - .5) / squash;
            float x = tex_coord0.x - 1. + T;

            if (0. < y && y < 1.) {
                for (n=0.; n < BLURMAX; n+=1.) {
                    x2 = x - n / resolution.x;
                    if (0. < x2 && x2 < 1.)
                        c += texture2D(tex_in, vec2(x2, y)) / BLURMAX;
                }
                gl_FragColor = mix(c, texture2D(tex_in, vec2(x, y)), pow(t, 5.));
            } else
                gl_FragColor = vec4(0, 0, 0, 0);
        }
    }
    '''  # noqa

    FAST_SLIDE_TRANSITION_DOWN = '''
    $HEADER$
    uniform float t;
    uniform sampler2D tex_in;
    uniform sampler2D tex_out;

    uniform vec2 resolution;

    float y2, n;
    float T = smoothstep(1., 0., t);
    float BLURMAX = 50.;
    void main(void){
        vec4 c = vec4(0., 0., 0., 0.);
        if (tex_coord0.y < 1. - T) {
            float squash = mix(.95, 1., pow(t, 2.));
            float x = .5 + (tex_coord0.x - .5) / squash;
            float y = tex_coord0.y + T;

            if (0. < x && x < 1.) {
                for (n=0.; n < BLURMAX; n+=1.) {
                    y2 = y - n / resolution.y;
                    if (0. <= y2 && y2 <= 1.)
                        c += texture2D(tex_in, vec2(x, y2)) / BLURMAX;
                }
                gl_FragColor = mix(c, texture2D(tex_in, vec2(x, y)), pow(t, 5.));
            } else
                gl_FragColor = vec4(0, 0, 0, 0);
        } else {
            float squash = mix(.95, 1., pow(1. - t, 2.));
            float x = .5 + (tex_coord0.x - .5) / squash;
            float y = tex_coord0.y - 1. + T;

            if (0. < x && x < 1.) {
                for (n=0.; n < BLURMAX; n+=1.) {
                    y2 = y - n / resolution.y;
                    if (0. <= y2 && y2 <= 1.)
                        c += texture2D(tex_out, vec2(x, y2)) / BLURMAX;
                }
                gl_FragColor = mix(c, texture2D(tex_out, vec2(x, y)), pow(1. - t, 5.));
            } else
                gl_FragColor = vec4(0, 0, 0, 0);
        }
    }
    '''  # noqa
    FAST_SLIDE_TRANSITION_RIGHT = '''
    $HEADER$
    uniform float t;
    uniform sampler2D tex_in;
    uniform sampler2D tex_out;

    uniform vec2 resolution;

    float x2, n;
    float T = smoothstep(1., 0., t);
    float BLURMAX = 50.;
    void main(void){
        vec4 c = vec4(0., 0., 0., 0.);
        if (tex_coord0.x < 1. - T) {
            float squash = mix(.95, 1., pow(t, 2.));
            float y = .5 + (tex_coord0.y - .5) / squash;
            float x = tex_coord0.x + T;

            if (0. < y && y < 1.) {
                for (n=0.; n < BLURMAX; n+=1.) {
                    x2 = x - n / resolution.x;
                    if (0. <= x2 && x2 <= 1.)
                        c += texture2D(tex_in, vec2(x2, y)) / BLURMAX;
                }
                gl_FragColor = mix(c, texture2D(tex_in, vec2(x, y)), pow(t, 5.));
            } else
                gl_FragColor = vec4(0, 0, 0, 0);
        } else {
            float squash = mix(.95, 1., pow(1. - t, 2.));
            float y = .5 + (tex_coord0.y - .5) / squash;
            float x = tex_coord0.x - 1. + T;

            if (0. < y && y < 1.) {
                for (n=0.; n < BLURMAX; n+=1.) {
                    x2 = x - n / resolution.x;
                    if (0. <= x2 && x2 <= 1.)
                        c += texture2D(tex_out, vec2(x2, y)) / BLURMAX;
                }
                gl_FragColor = mix(c, texture2D(tex_out, vec2(x, y)), pow(1. - t, 5.));
            } else
                gl_FragColor = vec4(0, 0, 0, 0);
        }
    }
    '''  # noqa
    fs = StringProperty()

    def __init__(self, **kwargs):
        self.on_direction(self, kwargs.get('direction', 'down'))
        super(FastSlideTransition, self).__init__(**kwargs)

    def on_progress(self, progress):
        self.render_ctx['resolution'] = [float(wh) for wh in self.screen_out.size]
        super(FastSlideTransition, self).on_progress(progress)

    def on_direction(self, *largs):
        if largs[1] == 'left':
            self.fs = self.FAST_SLIDE_TRANSITION_LEFT
        elif largs[1] == 'right':
            self.fs = self.FAST_SLIDE_TRANSITION_RIGHT
        elif largs[1] == 'up':
            self.fs = self.FAST_SLIDE_TRANSITION_UP
        elif largs[1] == 'down':
            self.fs = self.FAST_SLIDE_TRANSITION_DOWN


class ShatterTransition(ShaderTransition):
    direction = OptionProperty('left', options=('left', 'right', 'up', 'down'))
    '''Direction of the transition.

    :data:`direction` is an :class:`~kivy.properties.OptionProperty`, default
    to left. Can be one of 'left', 'right', 'up' or 'down'.
    '''
    rows = NumericProperty(10)
    cols = NumericProperty(10)

    SHATTER_TRANSITION_UP = '''
    $HEADER$
    uniform float t;
    uniform sampler2D tex_in;
    uniform sampler2D tex_out;
    uniform vec2 resolution;
    uniform float rows, cols;

    void main(void){
        float X, Y;
        X = floor(coords.x / cols);
        Y = floor(coords.y / rows);

    }
    '''

    def on_cols(self, *largs):
        self.render_ctx['cols'] = self.cols

    def on_rows(self, *largs):
        self.render_ctx['rows'] = self.rows

    def on_direction(self, *largs):
        if largs[1] == 'left':
            self.fs = self.SHATTER_TRANSITION_UP
        elif largs[1] == 'right':
            self.fs = self.SHATTER_TRANSITION_UP
        elif largs[1] == 'up':
            self.fs = self.SHATTER_TRANSITION_UP
        elif largs[1] == 'down':
            self.fs = self.SHATTER_TRANSITION_UP


class NavigationDrawerException(Exception):
    '''Raised when add_widget or remove_widget called incorrectly on a
    NavigationDrawer.

    '''


class NavigationDrawer(StencilView):
    '''Widget taking two children, a side panel and a main panel,
    displaying them in a way that replicates the popular Android
    functionality. See module documentation for more info.

    '''

    # Internal references for side, main and image widgets
    _side_panel = ObjectProperty()
    _main_panel = ObjectProperty()
    _join_image = ObjectProperty()

    side_panel = ObjectProperty(None, allownone=True)
    '''Automatically bound to whatever widget is added as the hidden panel.'''
    main_panel = ObjectProperty(None, allownone=True)
    '''Automatically bound to whatever widget is added as the main panel.'''

    # Appearance properties
    side_panel_width = NumericProperty()
    '''The width of the hidden side panel. Defaults to the minimum of
    250dp or half the NavigationDrawer width.'''
    separator_image = StringProperty('')
    '''The path to an image that will be placed between the side and main
    panels. If set to `''`, defaults to a gradient from black to
    transparent in an appropriate direction (left->right if side panel
    above main, right->left if main panel on top).'''
    separator_image_width = NumericProperty(dp(10))
    '''The width of the separator image. Defaults to 10dp'''

    # Touch properties
    touch_accept_width = NumericProperty('14dp')
    '''Distance from the left of the NavigationDrawer in which to grab the
    touch and allow revealing of the hidden panel.'''
    _touch = ObjectProperty(None, allownone=True)  # The currently active touch

    # Animation properties
    state = OptionProperty('closed', options=('open', 'closed'))
    '''Specifies the state of the widget. Must be one of 'open' or
    'closed'. Setting its value automatically jumps to the relevant state,
    or users may use the anim_to_state() method to animate the
    transition.'''
    anim_time = NumericProperty(0.3)
    '''The time taken for the panel to slide to the open/closed state when
    released or manually animated with anim_to_state.'''
    min_dist_to_open = NumericProperty(0.7)
    '''Must be between 0 and 1. Specifies the fraction of the hidden panel
    width beyond which the NavigationDrawer will relax to open state when
    released. Defaults to 0.7.'''
    _anim_progress = NumericProperty(0)  # Internal state controlling
                                         # widget positions
    _anim_init_progress = NumericProperty(0)

    # Animation controls
    top_panel = OptionProperty('main', options=['main', 'side'])
    '''Denotes which panel should be drawn on top of the other. Must be
    one of 'main' or 'side'. Defaults to 'main'.'''
    _main_above = BooleanProperty(True)

    side_panel_init_offset = NumericProperty(0.5)
    '''Intial offset (to the left of the widget) of the side panel, in
    units of its total width. Opening the panel moves it smoothly to its
    final position at the left of the screen.'''

    side_panel_darkness = NumericProperty(0.8)
    '''Controls the fade-to-black of the side panel in its hidden
    state. Must be between 0 (no fading) and 1 (fades to totally
    black).'''

    side_panel_opacity = NumericProperty(1)
    '''Controls the opacity of the side panel in its hidden state. Must be
    between 0 (fade to transparent) and 1 (no transparency)'''

    main_panel_final_offset = NumericProperty(1)
    '''Final offset (to the right of the normal position) of the main
    panel, in units of the side panel width.'''

    main_panel_darkness = NumericProperty(0)
    '''Controls the fade-to-black of the main panel when the side panel is
    in its hidden state. Must be between 0 (no fading) and 1 (fades to
    totally black).
    '''

    opening_transition = StringProperty('out_cubic')
    '''The name of the animation transition type to use when animating to
    an open state. Defaults to 'out_cubic'.'''

    closing_transition = StringProperty('in_cubic')
    '''The name of the animation transition type to use when animating to
    a closed state. Defaults to 'out_cubic'.'''

    anim_type = OptionProperty('reveal_from_below',
                               options=['slide_above_anim',
                                        'slide_above_simple',
                                        'fade_in',
                                        'reveal_below_anim',
                                        'reveal_below_simple',
                                        ])
    '''The default animation type to use. Several options are available,
    modifying all possibly animation properties including darkness,
    opacity, movement and draw height. Users may also (and are
    encouaged to) edit these properties individually, for a vastly
    larger range of possible animations. Defaults to reveal_below_anim.
    '''

    def __init__(self, **kwargs):
        super(NavigationDrawer, self).__init__(**kwargs)
        Clock.schedule_once(self.on__main_above, 0)

    def on_anim_type(self, *args):
        anim_type = self.anim_type
        if anim_type == 'slide_above_anim':
            self.top_panel = 'side'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 0.5
            self.main_panel_darkness = 0.5
            self.side_panel_init_offset = 1
        if anim_type == 'slide_above_simple':
            self.top_panel = 'side'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 0
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 1
        elif anim_type == 'fade_in':
            self.top_panel = 'side'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 0
            self.main_panel_final_offset = 0
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 0.5
        elif anim_type == 'reveal_below_anim':
            self.top_panel = 'main'
            self.side_panel_darkness = 0.8
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 1
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 0.5
        elif anim_type == 'reveal_below_simple':
            self.top_panel = 'main'
            self.side_panel_darkness = 0
            self.side_panel_opacity = 1
            self.main_panel_final_offset = 1
            self.main_panel_darkness = 0
            self.side_panel_init_offset = 0

    def on_top_panel(self, *args):
        if self.top_panel == 'main':
            self._main_above = True
        else:
            self._main_above = False

    def on__main_above(self, *args):
        newval = self._main_above
        main_panel = self._main_panel
        side_panel = self._side_panel
        self.canvas.remove(main_panel.canvas)
        self.canvas.remove(side_panel.canvas)
        if newval:
            self.canvas.insert(0, main_panel.canvas)
            self.canvas.insert(0, side_panel.canvas)
        else:
            self.canvas.insert(0, side_panel.canvas)
            self.canvas.insert(0, main_panel.canvas)

    def toggle_main_above(self, *args):
        if self._main_above:
            self._main_above = False
        else:
            self._main_above = True

    def add_widget(self, widget):
        if len(self.children) == 0:
            super(NavigationDrawer, self).add_widget(widget)
            self._side_panel = widget
        elif len(self.children) == 1:
            super(NavigationDrawer, self).add_widget(widget)
            self._main_panel = widget
        elif len(self.children) == 2:
            super(NavigationDrawer, self).add_widget(widget)
            self._join_image = widget
        elif self.side_panel is None:
            self._side_panel.add_widget(widget)
            self.side_panel = widget
        elif self.main_panel is None:
            self._main_panel.add_widget(widget)
            self.main_panel = widget
        else:
            raise NavigationDrawerException(
                'Can\'t add more than two widgets'
                'directly to NavigationDrawer')

    def remove_widget(self, widget):
        if widget is self.side_panel:
            self._side_panel.remove_widget(widget)
            self.side_panel = None
        elif widget is self.main_panel:
            self._main_panel.remove_widget(widget)
            self.main_panel = None
        else:
            raise NavigationDrawerException(
                'Widget is neither the side or main panel, can\'t remove it.')

    def set_side_panel(self, widget):
        '''Removes any existing side panel widgets, and replaces them with the
        argument `widget`.
        '''
        # Clear existing side panel entries
        if len(self._side_panel.children) > 0:
            for child in self._side_panel.children:
                self._side_panel.remove(child)
        # Set new side panel
        self._side_panel.add_widget(widget)
        self.side_panel = widget

    def set_main_panel(self, widget):
        '''Removes any existing main panel widgets, and replaces them with the
        argument `widget`.
        '''
        # Clear existing side panel entries
        if len(self._main_panel.children) > 0:
            for child in self._main_panel.children:
                self._main_panel.remove_widget(child)
        # Set new side panel
        self._main_panel.add_widget(widget)
        self.main_panel = widget

    def on__anim_progress(self, *args):
        if self._anim_progress > 1:
            self._anim_progress = 1
        elif self._anim_progress < 0:
            self._anim_progress = 0
        if self._anim_progress >= 1:
            self.state = 'open'
        elif self._anim_progress <= 0:
            self.state = 'closed'

    def on_state(self, *args):
        Animation.cancel_all(self)
        if self.state == 'open':
            self._anim_progress = 1
        else:
            self._anim_progress = 0

    def anim_to_state(self, state):
        '''If not already in state `state`, animates smoothly to it, taking
        the time given by self.anim_time. State may be either 'open'
        or 'closed'.

        '''
        if state == 'open':
            anim = Animation(_anim_progress=1,
                             duration=self.anim_time,
                             t=self.closing_transition)
            anim.start(self)
        elif state == 'closed':
            anim = Animation(_anim_progress=0,
                             duration=self.anim_time,
                             t=self.opening_transition)
            anim.start(self)
        else:
            raise NavigationDrawerException(
                'Invalid state received, should be one of `open` or `closed`')

    def toggle_state(self, animate=True):
        '''Toggles from open to closed or vice versa, optionally animating or
        simply jumping.'''
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'
        elif self.state == 'closed':
            if animate:
                self.anim_to_state('open')
            else:
                self.state = 'open'

    def on_touch_down(self, touch):
        col_self = self.collide_point(*touch.pos)
        col_side = self._side_panel.collide_point(*touch.pos)
        col_main = self._main_panel.collide_point(*touch.pos)

        if self._anim_progress < 0.001:  # i.e. closed
            valid_region = (self.x <=
                            touch.x <=
                            (self.x + self.touch_accept_width))
            if not valid_region:
                self._main_panel.on_touch_down(touch)
                return False
        else:
            if col_side and not self._main_above:
                self._side_panel.on_touch_down(touch)
                return False
            valid_region = (self._main_panel.x <=
                            touch.x <=
                            (self._main_panel.x + self._main_panel.width))
            if not valid_region:
                if self._main_above:
                    if col_main:
                        self._main_panel.on_touch_down(touch)
                    elif col_side:
                        self._side_panel.on_touch_down(touch)
                else:
                    if col_side:
                        self._side_panel.on_touch_down(touch)
                    elif col_main:
                        self._main_panel.on_touch_down(touch)
                return False
        Animation.cancel_all(self)
        self._anim_init_progress = self._anim_progress
        self._touch = touch
        touch.ud['type'] = self.state
        touch.ud['panels_jiggled'] = False  # If user moved panels back
                                            # and forth, don't default
                                            # to close on touch release
        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch is self._touch:
            dx = touch.x - touch.ox
            self._anim_progress = max(0, min(self._anim_init_progress +
                                            (dx / self.side_panel_width), 1))
            if self._anim_progress < 0.975:
                touch.ud['panels_jiggled'] = True
        else:
            super(NavigationDrawer, self).on_touch_move(touch)
            return

    def on_touch_up(self, touch):
        if touch is self._touch:
            self._touch = None
            init_state = touch.ud['type']
            touch.ungrab(self)
            jiggled = touch.ud['panels_jiggled']
            if init_state == 'open' and not jiggled:
                if self._anim_progress >= 0.975:
                        self.anim_to_state('closed')
                else:
                    self._anim_relax()
            else:
                self._anim_relax()
        else:
            super(NavigationDrawer, self).on_touch_up(touch)
            return

    def _anim_relax(self):
        '''Animates to the open or closed position, depending on whether the
        current position is past self.min_dist_to_open.

        '''
        if self._anim_progress > self.min_dist_to_open:
            self.anim_to_state('open')
        else:
            self.anim_to_state('closed')

    def _choose_image(self, *args):
        '''Chooses which image to display as the main/side separator, based on
        _main_above.'''
        if self.separator_image:
            return self.separator_image
        if self._main_above:
            return 'navigationdrawer_gradient_rtol.png'
        else:
            return 'navigationdrawer_gradient_ltor.png'