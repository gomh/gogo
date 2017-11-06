import game_framework
import title_state
from pico2d import *


name = "StartState"
image = None
Character = None
Grass = None
X = 400
Y = 0
Check = False
Check2 = False
logo_time = 0.0
Speed = 1

PauseImage = None

Pause = False
TTT = False
frame = 0




def enter():
    global image, Character, Grass, PauseImage
    open_canvas()
    image = load_image('kpu_credit.png')
    Character = load_image('yosi.png')
    Grass = load_image('grass.png')
    PauseImage = load_image('pause.png')



def exit():
    global image
    del(image)
    close_canvas()



def update():
    global logo_time, image, Check, X, Y, Check2, frame, Speed, Pause, TTT



    if(Pause == False):
        frame = 0
        if(frame > 1):
            frame = 0

        Y = 90
        X += Speed * 5

        if X > 790 :
            Speed *= -1

        if X < 10 :
            Speed *= -1


    if(logo_time > 2):
        logo_time = 0
        if TTT == False:
            TTT = True
        elif TTT == True:
            TTT = False
        #game_framework.quit()
        #game_framework.change_state(title_state)
        if(Check == False):
            image = load_image('title.png')
            Check = True
        elif Check == True and Check2 == False:
            Check2 = True

        #print('dd')


    delay(0.1)
    logo_time += 0.1




def draw():
    global image, Character, Grass, X, Y, Check, frame, PauseImage, Pause
    clear_canvas()

    if Pause == True and TTT == True:
        PauseImage.draw(400, 300)

    if(Check2 == False):
        image.draw(400, 300)

    elif Check2 == True:
        Grass.draw(400, 30)
        Character.clip_draw(frame * 100, 0, 100, 100, X, Y)

    update_canvas()




def handle_events():
    global Pause
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if Pause == False:
                Pause = True
            elif Pause == True:
                Pause = False


def pause(): pass


def resume(): pass





