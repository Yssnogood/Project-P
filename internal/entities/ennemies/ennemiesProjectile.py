import pygame as pg
from internal.game.settings import *

vec = pg.math.Vector2


class EnemyProjectile(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites, game.ennemies_projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Create projectile image
        self.image = pg.Surface((10, 10), pg.SRCALPHA)
        pg.draw.circle(self.image, RED, (5, 5), 5)
        self.rect = self.image.get_rect(center=(x, y))

        self.pos = vec(x, y)
        self.vel = direction * 100  # Direction normalized * speed

        self.damage = 1

    def update(self):
        # Update position
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        # Remove projectile if it goes off-screen
        if (self.rect.top < 0 or self.rect.bottom > HEIGHT or
            self.rect.left <= POS_GAME_X_BEGAN or self.rect.right >= POS_GAME_X_END):
            self.kill()
