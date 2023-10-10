import os
import sys
import kivy
import random
from time import strftime
#
from app_config import w_frame
from app_search import search
from app_control import (listener_mouse, 
                         listener_keyboard,
                         k_press, k_release,
                         m_click, m_move,
                         copy_selection)
#
from kivy.config import Config
Config.set('graphics', 'borderless', str(w_frame))
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '400')
Config.set('graphics', 'resizable', '1')
Config.set('kivy','window_icon','./icons/eye-arrow-right-outline.png')
#
from kivy import platform
from kivy.app import App
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.uix.button import (Button, ButtonBehavior)
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.actionbar import ActionButton
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
from kivy.properties import (NumericProperty, 
                             ObjectProperty, 
                             StringProperty, 
                             ColorProperty, 
                             BooleanProperty, 
                             Clock)


class MainScreen(BoxLayout):    
    exit_footer_text = StringProperty('Press the Esc Key to Exit the App or this button ->')
    exit_text = StringProperty('See You Later!')
    tbtn_state = StringProperty(str(w_frame))
    input_txt = StringProperty('')
    status_txt = StringProperty('Welcome!')
    kwph_txt = NumericProperty(int(str(0)))
    current_time = StringProperty(strftime("%I:%M:%S %p"))
    elapsed_time = NumericProperty(int(str(60)))
    MAX_KWPH = NumericProperty(120)
    t_dt = NumericProperty(0)
    flag = ObjectProperty(False)



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        listener_mouse.start()
        listener_keyboard.start()
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.copy_kw, 0.1)

    def update_time(self, dt):
        self.current_time = strftime("%I:%M:%S %p")
        if dt > 1 or dt < 1:
            dt = 1
            self.t_dt += dt
            if (self.t_dt % 60) == 0:
                self.elapsed_time - self.t_dt
                self.elapsed_time -= 1
        if self.elapsed_time == 0:
            self.elapsed_time = 60
        self.kwph_txt = (self.elapsed_time / 60) * self.MAX_KWPH


    def copy_kw(self, *args):
            if k_press[0] == m_click[0] == m_move[0] == 1:
                print('in while loop')
                self.flag = True
                copy_selection()
            if k_press[0] == m_click[0] == 0:
                if self.flag == True:
                    self.paste_kw()
                else:
                    pass


    def paste_kw(self, *args):
        self.flag = False
        try:
            if k_release[0] == 1:
                print('that\'s something')
                key_word = Clipboard.paste()
                search_paste = search(kw=key_word)
                self.input_txt = (f'You were searching for -> {key_word}\n\nWith the result of -> {search_paste}')
                self.status_txt = 'Results In: '
        except AttributeError:
            print('try again!')



    def borderless(self, get_state):
        self.frameless = w_frame
        self.status_txt = 'Restarting...'
        if get_state.state == 'down':
            with open('app_config.py', 'w') as f:
                self.frameless = '1'
                f.write(f'w_frame = {self.frameless}')
            Clock.schedule_once(self.restart, 0.5)
            self.ids.tbtn_state = 'down'
        if get_state.state == 'normal':
            with open('app_config.py', 'w') as f:
                self.frameless = '0'
                f.write(f'w_frame = {self.frameless}')
            Clock.schedule_once(self.restart, 0.5)
            self.ids.tbtn_state = 'normal'

    
    def restart(self, *args):
        os.execvp(sys.executable, ['python'] + sys.argv)


    def animate(self):
        anim = Animation(x=-1, duration=1.5, opacity=0, step= 1/60)
        anim.start(self.ids.exit_label)


    def exit_btn(self, get_state):
        if get_state.state == 'down':
            self.exit_footer_text = self.exit_text
            listener_mouse.stop()
            listener_keyboard.stop()
            Clock.schedule_once(self.exit_app, 0)
        else:
            return f'State: {get_state.state}'
        
        
    def exit_app(self, *args):
        if self.ids.exit_label.text == self.exit_text:
            self.animate()
            Clock.schedule_once(EyeSearchApp().stop, 1.5)


class EyeSearchApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    def build(self):
        self.title = 'EyeSearch - quicker key-word Google search!'
        Builder.load_file('main.kv')
        return MainScreen()
    

    def stop(self, *largs):
        return super().stop(*largs)


if __name__ == '__main__':
    if platform in ('linux', 'win', 'macosx'):
        EyeSearchApp().run()
        





