import game_framework
from pico2d import *


name = "StartState"
image = None
logo_image = None
logo_time = 0.0


def enter():
    global logo_image, image
    open_canvas(800, 500,True)
    image = load_image('kpu_credit.png')


def exit():
    global logo_image, image
    del(image)

import title_state

def update():
    global logo_time

    if (logo_time >1.0):
        logo_time=0
        game_framework.change_state(title_state)
    delay(0.01)
    logo_time +=0.01




def draw():
    global logo_image, image
    clear_canvas()
    image.draw(400,300)
    update_canvas()


def handle_events():
    events = get_events()



def pause(): pass


def resume(): pass


