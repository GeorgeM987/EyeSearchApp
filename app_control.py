import pynput
from pynput import mouse, keyboard
from pynput.mouse import Listener
from pynput.keyboard import Listener, Key, Controller

keyb = Controller()


m_move = [0]
sum_move = []
xy_sum_lower = []
xy_sum_higher = []
def on_move(x, y):
    xy_sum = (x + y)
    for i in range(0, 10):
        sum_move.append(xy_sum)
        xy_sum_lower.append(xy_sum - 1)
        xy_sum_higher.append(xy_sum + 1)
    sum_move_average = int(sum(sum_move) / len(sum_move))
    if (sum_move_average in xy_sum_lower) or (sum_move_average in xy_sum_higher):
        m_move[0] = 1
    else:
        m_move[0] = 0


m_click = [0]
def on_click(x, y, button, pressed):
    if pressed:
        m_click[0] = 1
    else:
        m_click[0] = 0


k_press = [0]
k_release = [0]
def on_press(key):
    if 'ctrl' in str(key):
        k_press[0] = 1
        k_release[0] = 0
    else:
        k_press[0] = 0


def on_release(key):
    if 'ctrl' in str(key):
        k_press[0] = 0
        k_release[0] = 1
    else:
        k_release[0] = 0
    

def copy_selection():
    with keyb.pressed(Key.ctrl.value):
        keyb.press('c')
        keyb.release('c')


listener_mouse = mouse.Listener(on_move=on_move, on_click=on_click)
listener_keyboard = keyboard.Listener(on_press=on_press, on_release=on_release)


if __name__ == '__main__':
    copy_selection()