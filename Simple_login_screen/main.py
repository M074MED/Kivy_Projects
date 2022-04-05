from kivy.app import App
from kivy.core.window import Window

Window.clearcolor = (0.3, 0.7, 0.4)
Window.size = (400, 620)


class Main(App):
    def build(self):
        self.title = "Login Screen"
        pass


Main().run()
