from kivy.animation import Animation
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image


class MyImage(Image):
    def __init__(self, **kwargs):
        super(MyImage, self).__init__(**kwargs)
        self.frame_counter = 0
        self.frame_number = 8  # my example GIF had 2 frames

    def on_texture(self, instance, value):
        if self.frame_counter == self.frame_number + 1:
            self._coreimage.anim_reset(False)
        self.frame_counter += 1


class MyAnimation(Animation):
    def __init__(self, image, **kwargs):
        super(MyAnimation, self).__init__(**kwargs)
        self.image = image

    def on_start(self, widget):
        self.image._coreimage.anim_reset(True)

    def on_complete(self, widget):
        self.image._coreimage.anim_reset(False)


class Test(App):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)

        self.content = BoxLayout()
        self.content.orientation = 'vertical'
        self.anim_image = MyImage(source='set/right.zip')
        self.anim_button = Button(on_press=self.animate_image)
        self.content.add_widget(self.anim_image)
        self.content.add_widget(self.anim_button)
        self.anim_image.anim_delay = -1

    def build(self):
        return self.content

    def stop_anims(self):
        self.anim_image.anim_delay = -1

    def animate_image(self, *args, **kwargs):
        image_animate = MyAnimation(image=self.anim_image)
        self.anim_image.anim_delay = 0.1

        def f(i, w):
            w.source = 'image%d.png' % i

        for i in range(4):
            a = Animation(x=(i * 20), duration=(0.10 * i))
            image_animate += a

        image_animate.start(self.anim_image)



if __name__ == '__main__':
    Test().run()
