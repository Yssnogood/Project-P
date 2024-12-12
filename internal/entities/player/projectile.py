import pygame as pg
from internal.game.settings import *

vec = pg.math.Vector2


class Projectile(pg.sprite.Sprite):
    def __init__(self, game, x, y, owner, damage=10, angle=0):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.angle = angle
        self.pos = vec(x, y)
        self.vel = vec(0, -PROJECTILE_SPEED) if owner == "player" else vec(0, PROJECTILE_SPEED) # Par défaut, va vers le haut
        self.rect.center = self.pos

        self.owner = owner

        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt 
        self.pos.x += self.angle
        self.rect.center = self.pos

        # Supprime le projectile s'il sort de l'écran
        if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.rect.right > POS_GAME_X_END or self.rect.left < POS_GAME_X_BEGAN:
            self.kill()