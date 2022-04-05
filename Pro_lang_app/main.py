from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

Window.clearcolor = (100/255, 0, 1, 1)
Window.size = (400, 630)

class WindowManager(ScreenManager):
  pass
class MainScreen(Screen):
  pass
class SecondScreen(Screen):
  pass
class ErrorScreen(Screen):
  pass
class PythonScreen(Screen):
  pass
class PerlScreen(Screen):
  pass
class PHPScreen(Screen):
  pass
class SQLScreen(Screen):
  pass
class HTMLScreen(Screen):
  pass
class CSSScreen(Screen):
  pass

kv = Builder.load_file("main.kv")
class Main(App):
  def build(self):
    self.title = "Programming Language App"
    return kv
if __name__ == '__main__':
  Main().run()