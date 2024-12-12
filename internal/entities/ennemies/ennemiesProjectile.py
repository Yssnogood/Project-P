import pygame as pg
from internal.game.settings import *

vec = pg.math.Vector2


class EnemyProjectile(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites, game.ennemies_projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.vel = direction * 100  # Direction normalisée * vitesse

        self.domage = 1

    def update(self):
        
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        # Si le projectile sort de l'écran, on le supprime
        if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.rect.left <= POS_GAME_X_BEGAN or self.rect.right >= POS_GAME_X_END:
            self.kill()
