import pygame as pg
from internal.game.settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((50, 50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y)
        
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        
        if self.pos.x > POS_GAME_X_END - self.rect.width:
            self.pos.x = POS_GAME_X_END - self.rect.width
        if self.pos.x < POS_GAME_X_BEGAN:
            self.pos.x = POS_GAME_X_BEGAN
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > HEIGHT - self.rect.height:
            self.pos.y = HEIGHT - self.rect.height

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y