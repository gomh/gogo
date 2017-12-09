import game_framework
import main_state
from pico2d import *

name = "TitleState"
logo_image = None

def enter():
    global logo_image
    logo_image = load_image('title.png')


def exit():
    global logo_image
    del(logo_image)


def handle_events():
    global skip
    events = get_events()
    for event in events:
        if event.type is SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key)==(SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)



def draw():
    clear_canvas()
    logo_image.draw(400, 300)
    update_canvas()

def update():
    pass


def pause():
    pass


def resume():
    pass






