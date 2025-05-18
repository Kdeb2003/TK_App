from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ColorProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard

KV = '''
<MyCustomCard>:
    size_hint: None, None
    size: "280dp", "180dp"
    pos_hint: {"center_x": .5, "center_y": .5}
    shadow_color: 1, 0, 0, 1  # Red color

    canvas.before:
        Color:
            rgba: self.shadow_color
        Rectangle:
            size: self.size
            pos: self.pos

Screen:
    MyCustomCard:
        elevation: 5
'''

class MyCustomCard(MDCard):
    shadow_color = ColorProperty([0, 0, 0, 1])

class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

TestApp().run()
