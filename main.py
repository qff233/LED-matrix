from driver import Light, Touch
from imgs import get_img
from snake import Snake
from tetris import Tetris

from front3x5 import add_front

light = Light()
touch = Touch()

snake = Snake()
tetris = Tetris()     

def show_hello():
    img = [[(0,0,0) for col in range(12)] for row in range(10)]
    add_front(img, (0,0), "H")
    add_front(img, (4,0), "E")
    add_front(img, (8,0), "L")
    add_front(img, (0,5), "L")
    add_front(img, (4,5), "O")
    light.show(img)

show_hello()

while True:
    if touch.is_touch(0):
        light.show(get_img(0))
    elif touch.is_touch(1):
        light.show(get_img(1))
    elif touch.is_touch(2):
        snake.main_loop(light,touch)
        show_hello()
    elif touch.is_touch(3):
        tetris.main_loop(light, touch)
        show_hello()
    elif touch.is_touch(4):
        show_hello()
    elif touch.is_touch(5):
        show_hello()
    elif touch.is_touch(6):
        show_hello()
    elif touch.is_touch(7):
        show_hello()
    elif touch.is_touch(8):
        show_hello()
    elif touch.is_touch(9):
        show_hello()

