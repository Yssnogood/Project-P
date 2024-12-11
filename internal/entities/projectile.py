import pygame as pg
from internal.game.settings import *

vec = pg.math.Vector2


class Projectile(pg.sprite.Sprite):
    def __init__(self, game, x, y, owner):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, -PROJECTILE_SPEED) if owner == "player" else vec(0, PROJECTILE_SPEED) # Par défaut, va vers le haut
        self.rect.center = self.pos

        self.owner = owner

        self.domage = 10

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        # Supprime le projectile s'il sort de l'écran
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()