import pygame as pg
from internal.game.settings import *
from internal.entities.player.projectile import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y)

        self.last_shot = 0
        self.last_bomb = 0

        self.health = 5
        self.bombCounter = 5
        
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

        if keys[pg.K_LSHIFT]:
            self.vel *= 0.5

        if keys[pg.K_a]:
            now = pg.time.get_ticks()
            if self.bombCounter >0 and now - self.last_bomb > 400 :
                self.last_bomb = now
                self.bomb()
                self.bombCounter -= 1
    
        if keys[pg.K_SPACE] :
            self.shoot()
            self.shoot_triangle()

    def take_damage(self, amount):
        self.health -= amount
        print("New player hp : ", self.health)
        for projectile in self.game.ennemies_projectiles:
            projectile.kill()
        if self.health <=0:
            self.kill()
            print("Player has been slayed")

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 250:
            self.last_shot = now
            proj = Projectile(self.game, self.rect.centerx, self.rect.top, "player")
            self.game.player_projectiles.add(proj)
            
    def shoot_triangle(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 150:
            self.last_shot = now
            proj = Projectile(self.game, self.rect.centerx, self.rect.top, "player",3)
            self.game.player_projectiles.add(proj)
            
            proj = Projectile(self.game, self.rect.centerx, self.rect.top, "player",3, 2)
            self.game.player_projectiles.add(proj)

            proj = Projectile(self.game, self.rect.centerx, self.rect.top, "player",3, -2)
            self.game.player_projectiles.add(proj)
        
    def bomb(self):
        print("Bomb was trigger")
        for fairy in self.game.all_fairy:
            fairy.take_damage(6)
        for projectile in self.game.ennemies_projectiles:
            projectile.kill()

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
