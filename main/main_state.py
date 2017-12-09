import game_framework
import title_state
from pico2d import *
import random

class Yosi:
    def __init__(self):
        ##############################################################
        #       기본값     #
        self.initDrawX, self.initDrawY = 50, 107
        self.maxJumpHeight = 130
        self.defaultRunningSpeed = 11
        self.jumpSpeed = 20
        self.maxDashSec = 2
        self.dashPower = 2
        self.maxLife = 3
        ##############################################################

        self.worldX, self.worldY = 0,0
        self.curDrawX, self.curDrawY = self.initDrawX, self.initDrawY

        self.curLife = self.maxLife
        self.curRunningSpeed = self.defaultRunningSpeed
        self.curDashSec = 0
        self.frame = 0
        self.jump_dir = 1.2

        self.jumping = False
        self.dash = False

        self.eat_sound = None

        if self.eat_sound == None:
            self.eat_sound = load_wav('pickup.wav')
            self.eat_sound.set_volume(32)

    def eat(self, egg):
        self.eat_sound.play()

    def prepare_image(self):
        self.yosi_image = load_image('run_animation_yosi.png')
        self.dash_image = load_image('dash.png')
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

        if self.jumping == True:
            self.curDrawY += self.jumpSpeed * self.jump_dir
            self.worldY = self.curDrawY
            if self.curDrawY > self.initDrawY + self.maxJumpHeight:
                self.jump_dir = -1
            elif self.curDrawY < self.initDrawY:
                self.worldY = self.curDrawY = self.initDrawY
                self.jump_dir = 1.2
                self.jumping = False

        if self.dash == True:
            self.curDashSec += frame_time
            if self.curDashSec > self.maxDashSec:
                self.curDashSec = 0
                self.dash = False
                self.curRunningSpeed = self.defaultRunningSpeed

    def draw(self):
        if self.dash == True:
            self.frame %= 2
            self.dash_image.clip_draw(self.frame * 100, 0, 100, 100, self.curDrawX, self.curDrawY-13)

        else:
            self.yosi_image.clip_draw(self.frame * 100, 0, 100, 100, self.curDrawX, self.curDrawY)

        canvas_h = get_canvas_height()
        for i in range(self.curLife):
            self.life_image.clip_draw(0, 0, 50, 50, 40 + 60 * i, canvas_h * 0.90)

    def get_bb(self):
        if self.dash == True:
            return self.curDrawX - 25, self.curDrawY - 25, self.curDrawX + 25, self.curDrawY + 10
        else:
            return self.curDrawX - 25, self.curDrawY - 25, self.curDrawX + 25, self.curDrawY + 25

class Background:
    def __init__(self):
        self.ground_image = None
        self.sky_image = None
        self.bush1_image = None
        self.bush2_image = None
        self.block_image = None
        self.left = 0
        self.bgm = load_music('football.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        ##############################################################
        #       기본값     #
        self.ground_w = 800
        self.ground_h = 75
        self.sky_w = 800
        self.sky_h = 600
        self.bush1_w = 1942
        self.bush1_h = 21
        self.bush2_w = 2287
        self.bush2_h = 84
        self.block_w = 2371
        self.block_h = 168
        ##############################################################

    def prepare_image(self):
        self.ground_image = load_image('ground.png')
        self.sky_image = load_image('back.png')
        self.bush1_image = load_image('bush1.png')
        self.bush2_image = load_image('bush2.png')
        self.block_image = load_image('block.png')

    def draw(self):
        ground_x = int(self.left % self.ground_image.w)
        bush1_x = int((self.left * 3.5) % self.bush1_image.w)
        bush2_x =int((self.left * 3.0) % self.bush2_image.w)
        sky_x = int((self.left * 1.5) % self.sky_image.w)
        block_x = int((self.left * 2) % self.block_image.w)

        s_w = min(self.sky_image.w - sky_x, self.sky_w)
        self.sky_image.clip_draw_to_origin(sky_x, 0, s_w, self.sky_h, 0, 0)
        self.sky_image.clip_draw_to_origin(0, 0, self.sky_w - s_w, self.sky_h, s_w, 0)

        bl_w = min(self.block_image.w - block_x, self.block_w)
        self.block_image.clip_draw_to_origin(block_x, 0, bl_w, self.block_h, 0, 74)
        self.block_image.clip_draw_to_origin(0, 0, self.block_w - bl_w, self.block_h, bl_w, 74)

        b2_w = min(self.bush2_image.w - bush2_x, self.bush2_w)
        self.bush2_image.clip_draw_to_origin(bush2_x, 0, b2_w, self.bush2_h, 0, 74)
        self.bush2_image.clip_draw_to_origin(0, 0, self.bush2_w - b2_w, self.bush2_h, b2_w, 74)

        b1_w = min(self.bush1_image.w - bush1_x, self.bush1_w)
        self.bush1_image.clip_draw_to_origin(bush1_x, 0, b1_w, self.bush1_h, 0, 74)
        self.bush1_image.clip_draw_to_origin(0, 0, self.bush1_w - b1_w, self.bush1_h, b1_w, 74)

        g_w = min(self.ground_image.w - ground_x, self.ground_w)
        self.ground_image.clip_draw_to_origin(ground_x, 0, g_w, self.ground_h, 0, 0)
        self.ground_image.clip_draw_to_origin(0, 0, self.ground_w - g_w, self.ground_h, g_w, 0)

    def update(self, frame_time, yosiSpeed):
        self.left = (self.left + frame_time * yosiSpeed)

    def __del__(self):
        del self.bgm

class Egg:
    def __init__(self,x):
        self.image = None
        #######################################
        #       기본값     #
        self.initY = 100
        #######################################
        self.initX = x
        self.curDrawX = self.initX
        self.curDrawY = self.initY
        self.available = True

    def prepare_image(self):
        self.image = load_image('egg.png')

    def update(self):
        pass

    def draw(self, yosiX):
        self.curDrawX = self.initX - yosiX
        self.image.clip_draw(0, 0, 35, 38, self.curDrawX, self.curDrawY)

    def get_bb(self):
        return self.curDrawX - 16, self.curDrawY - 16, self.curDrawX + 16, self.curDrawY + 16

class Flower:
    def __init__(self,x):
        self.image = None
        ##############################################################
        #       기본값     #
        self.initY = 100
        ##############################################################
        self.initX = x
        self.curDrawX = self.initX
        self.curDrawY = self.initY
        self.available = True
        self.frame = 0

    def prepare_image(self):
        self.image = load_image('flower1.png')

    def update(self):
        self.frame = (self.frame + 1) % 2

    def draw(self, yosiX):
        self.curDrawX = self.initX - yosiX
        self.image.clip_draw(self.frame*100, 0, 100, 102, self.curDrawX, self.curDrawY)

    def get_bb(self):
        return self.curDrawX - 20, self.curDrawY - 25, self.curDrawX + 20, self.curDrawY + 25

class Ghost:
    def __init__(self,x):
        self.image = None
        ##############################################################
        #       기본값     #
        self.initY = 250
        ##############################################################
        self.initX = x
        self.curDrawX = self.initX
        self.curDrawY = self.initY
        self.available = True
        self.frame = 0

    def prepare_image(self):
        self.image = load_image('ghost.png')

    def update(self):
        self.frame = (self.frame + 1) % 3

    def draw(self,yosiX):
        self.curDrawX = self.initX - yosiX
        self.image.clip_draw(self.frame*72, 0, 72, 64, self.curDrawX, self.curDrawY)

    def get_bb(self):
        return self.curDrawX - 36, self.curDrawY - 32, self.curDrawX + 36, self.curDrawY + 32

name = "StartState"

PauseImage = None

Pause = False
TTT = False
frame = 0
yosi = None
background = None
flowerList = []
ghostList = []
eggList = []

def enter():
    global PauseImage, flowerList, ghostList, eggList, yosi, background

    yosi=Yosi()
    background = Background()

    for i in range(1000):
        if random.random() > 0.4:
            flowerList.append(Flower(1500+ i * 450))
        else:
            ghostList.append(Ghost(1500+i*450))

        if random.random() > 0.1:
            eggList.append(Egg(3000+i*450))


    PauseImage = load_image('pause.png')
    yosi.prepare_image()
    background.prepare_image()

    for flower in flowerList:
        flower.prepare_image()

    for ghost in ghostList:
        ghost.prepare_image()

    for egg in eggList:
        egg.prepare_image()

def exit():
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
    global frame, Pause, TTT, yosi
    delay(0.05)

    if(Pause == False):
        yosi.update(0.1)
        for egg in eggList:
            egg.update()

        for egg in eggList:
            if collide(yosi, egg):
                eggList.remove(egg)
                yosi.eat(egg)

        background.update(0.1,yosi.curRunningSpeed)


        for flower in flowerList:
            flower.update()
            if flower.available == True:
                if collide(yosi,flower) == True and yosi.curLife > 0:
                    yosi.curLife -= 1
                    flower.available = False
                    print(yosi.worldX + flower.curDrawX, "위치의 꽃과 충돌")

        for ghost in ghostList:
            ghost.update()
            if ghost.available == True:
                if collide(yosi,ghost) == True and yosi.curLife > 0:
                    yosi.curLife -= 1
                    ghost.available = False
                    print(yosi.worldX + ghost.curDrawX, "위치의 유령과 충돌")

        for egg in eggList:
            egg.update()
            if egg.available == True:
                if collide(yosi,egg) == True and yosi.curLife > 0:
                    egg.available = False
                    print(yosi.worldX + egg.curDrawX, "위치의 알을 먹음")

def draw():
    global Character, frame, PauseImage, Pause
    clear_canvas()

    if Pause == True and TTT == True:
        PauseImage.draw(400, 300)

    background.draw()
    for flower in flowerList:
        flower.draw(yosi.worldX)
        draw_rectangle(*flower.get_bb())
    for ghost in ghostList:
        ghost.draw(yosi.worldX)
        draw_rectangle(*ghost.get_bb())
    for egg in eggList:
        egg.draw(yosi.worldX)
        draw_rectangle(*egg.get_bb())

    yosi.draw()
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

def pause():
    pass

def resume():
    pass





