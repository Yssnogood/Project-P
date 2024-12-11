import pygame as pg
from internal.game.settings import *
from internal.entities.projectile import *

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

        self.last_shot = 0

        self.health = 50
        
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
    
        if keys[pg.K_SPACE] :
            self.shoot()

    def take_domage(self, amount):
        self.health -= amount
        print("New player hp : ", self.health)
        if self.health <=0:
            self.kill()
            print("Player has been slayed")

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 150:
            self.last_shot = now
            proj = Projectile(self.game, self.rect.centerx, self.rect.top, "player")
            self.game.player_projectiles.add(proj)

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
