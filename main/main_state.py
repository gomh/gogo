import game_framework
import title_state
from pico2d import *
import random


class Yosi:
    def __init__(self):
        ##############################################################
        #       기본값     #
        self.initDrawX, self.initDrawY = 40, 90
        self.maxJumpHeight = 100
        self.defaultRunningSpeed = 20
        self.jumpSpeed = 10
        self.maxDashSec = 2
        self.dashPower = 3
        self.maxLife = 3
        ##############################################################

        self.worldX, self.worldY = 0,0
        self.curDrawX, self.curDrawY = self.initDrawX, self.initDrawY

        self.curLife = self.maxLife
        self.curRunningSpeed = self.defaultRunningSpeed
        self.curDashSec = 0
        self.frame = 0
        self.dir = 1
        self.jumping = False
        self.dash = False

    def prepare_image(self):
        self.yosi_image = load_image('run_animation_yosi.png')
        self.life_image = load_image('mushroom.png')

    def handle_event(self, event):
        if event.key == SDLK_SPACE and self.jumping == False:
            self.jumping = True
        elif event.key == SDLK_a and self.dash == False:
            self.dash = True
            self.curRunningSpeed = self.defaultRunningSpeed * self.dashPower

    def update(self, frame_time):
        self.frame = (self.frame + 1) % 7
        self.worldX += self.curRunningSpeed
        #print("Yosi Position x:",self.worldX, "y:",self.worldY)
        if self.jumping == True:
            self.curDrawY += self.jumpSpeed * self.dir
            self.worldY = self.curDrawY
            if self.curDrawY > self.initDrawY + self.maxJumpHeight:
                self.dir = -1
            elif self.curDrawY < self.initDrawY:
                self.worldY = self.curDrawY = self.initDrawY
                self.dir = 1
                self.jumping = False

        if self.dash == True:
            self.curDashSec += frame_time
            if self.curDashSec > self.maxDashSec:
                self.curDashSec = 0
                self.dash = False
                self.curRunningSpeed = self.defaultRunningSpeed

    def draw(self):
        self.yosi_image.clip_draw(self.frame * 100, 0, 100, 100, self.curDrawX, self.curDrawY)
        canvas_h = get_canvas_height()
        for i in range(self.curLife):
            self.life_image.clip_draw(0, 0, 100, 100, 20+100 * i, canvas_h * 0.8)

    def get_bb(self):
        return self.curDrawX - 40, self.curDrawY - 40, self.curDrawX + 40, self.curDrawY + 40

class Background:
    def __init__(self):
        self.image = None
        self.left = 0
        ##############################################################
        #       기본값     #
        self.screen_width = 802
        self.screen_height = 62
        ##############################################################

    def prepare_image(self):
        self.image = load_image('grass.png')

    def draw(self):
        x = int(self.left)
        w = min(self.image.w - x, self.screen_width)
        self.image.clip_draw_to_origin(x, 0, w, self.screen_height, 0, 0)
        self.image.clip_draw_to_origin(0, 0, self.screen_width - w, self.screen_height, w, 0)

    def update(self, frame_time, yosiSpeed):
        self.left = (self.left + frame_time * yosiSpeed) % self.image.w

class Rock:
    def __init__(self,x):
        self.image = None
        ##############################################################
        #       기본값     #
        self.initY = 70
        ##############################################################
        self.initX = x
        self.curDrawX = self.initX
        self.curDrawY = self.initY
        self.available = True

    def prepare_image(self):
        self.image = load_image('flower1.png')

    def update(self):
        pass


    def draw(self,yosiX):
        self.curDrawX = self.initX - yosiX
        self.image.clip_draw(0, 0, 100, 102, self.curDrawX, self.curDrawY)

    def get_bb(self):
        return self.curDrawX - 13, self.curDrawY - 14, self.curDrawX + 13, self.curDrawY + 14


name = "StartState"
image = None
Check = False
Check2 = False
logo_time = 0.0
Speed = 1

PauseImage = None

Pause = False
TTT = False
frame = 0
yosi = Yosi()
background = Background()
rockList = []

def enter():
    global image, PauseImage, rockList
    open_canvas()
    image = load_image('kpu_credit.png')
    PauseImage = load_image('pause.png')
    yosi.prepare_image()
    background.prepare_image()

    for i in range(1000):
        if random.random() > 0.3:
            rockList.append(Rock(i*500))

    for rock in rockList:
        rock.prepare_image()

def exit():
    global image
    del(image)
    close_canvas()

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def update():
    global logo_time, image, Check, Check2, frame, Speed, Pause, TTT

    if(Pause == False):
        yosi.update(0.1)
        background.update(0.1,yosi.curRunningSpeed)

        # 충돌테스트
        for rock in rockList:
            if rock.available == True:
                if collide(yosi,rock) == True and yosi.curLife > 0:
                    yosi.curLife -= 1
                    rock.available = False
                    print(yosi.worldX + rock.curDrawX, "위치의 돌과 충돌")

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

    delay(0.1)
    logo_time += 0.1

def draw():
    global image, Character, Check, frame, PauseImage, Pause
    clear_canvas()

    if Pause == True and TTT == True:
        PauseImage.draw(400, 300)

    if(Check2 == False):
        image.draw(400, 300)

    elif Check2 == True:
        background.draw()
        yosi.draw()
        for rock in rockList:
            rock.draw(yosi.worldX)
            draw_rectangle(*rock.get_bb())
        draw_rectangle(*yosi.get_bb())

    update_canvas()



def handle_events():
    global Pause
    events = get_events()
    for event in events:
        if event.type is SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key== SDLK_p:
                if Pause == False:
                    Pause = True
                elif Pause == True:
                    Pause = False
            else:
                yosi.handle_event(event)


def pause(): pass


def resume(): pass





