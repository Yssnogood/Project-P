import pygame as pg
from internal.game.settings import *

vec = pg.math.Vector2

class Fairy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_fairy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((50, 50))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.memo = [x,y]
        self.vel = vec(0,0)
        self.pos = vec(x,y)
        self.switchDirec = [False,False,False]

    def left(self, speed):
        self.vel = vec(0,0)
        self.vel.x -=speed

    def right(self, speed):
        self.vel = vec(0,0)
        self.vel.x +=speed

    def up(self, speed):
        self.vel = vec(0,0)
        self.vel.y -=speed

    def down(self,speed):
        self.vel = vec(0,0)
        self.vel.y += speed

    def moveSqaure(self):
        if self.pos.x <= self.memo[0] and self.pos.x > self.memo[0] - 150 :
            self.left(50)

    def isInBorder(self):

        if self.pos.x > POS_GAME_X_END - self.rect.width:
            self.pos.x = POS_GAME_X_END - self.rect.width
        if self.pos.x < POS_GAME_X_BEGAN:
            self.pos.x = POS_GAME_X_BEGAN
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > HEIGHT - self.rect.height:
            self.pos.y = HEIGHT - self.rect.height

    def update(self):
        self.isInBorder()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
