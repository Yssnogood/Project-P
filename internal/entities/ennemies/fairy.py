import pygame as pg
from internal.game.settings import *
from internal.entities.ennemies.ennemiesProjectile import *
import math

vec = pg.math.Vector2

class Fairy(pg.sprite.Sprite):
    def __init__(self, game, x, y, pattern="zigzag", speed=10,radius=200 ):
        self.groups = game.all_sprites, game.all_fairy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((FAIRY_SIZE, FAIRY_SIZE), pg.SRCALPHA)
        pg.draw.circle(self.image, (0, 255, 0), (25, 25), 25)
        self.rect = self.image.get_rect()

        self.last_shot_time = 0
        self.shoot_delay = 300

        self.pos = vec(x, y)
        self.center = vec(x, y)  # Centre pour les mouvements circulaires
        self.angle = 0  # Angle pour le pattern circulaire
        self.radius = radius
        self.speed = speed
        self.direction = vec(1, 0)  # Direction pour le mouvement linéaire
        self.pattern = pattern  # Type de déplacement
        self.health = 30

    def take_domage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            print("A fairy has been killed")

    def shoot(self):
        # Calculer la direction vers le joueur
        player_pos = self.game.player.rect.center
        fairy_pos = vec(self.rect.center)
        direction = (player_pos - fairy_pos).normalize()  # Direction normalisée vers le joueur

        now = pg.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            EnemyProjectile(self.game, self.rect.centerx, self.rect.centery, direction)

    def move_circle(self):
        self.angle += self.speed * self.game.dt
        if self.angle >= 2 * math.pi:
            self.angle = 0
        self.pos.x = self.center.x + self.radius * math.cos(self.angle)
        self.pos.y = self.center.y + self.radius * math.sin(self.angle)

    def move_zigzag(self):
        if self.pos.x > POS_GAME_X_END - self.rect.width:
            self.speed *= -1
        if self.pos.x < POS_GAME_X_BEGAN:
            self.speed *= -1

        self.pos.x += self.speed * self.game.dt * 50
        self.pos.y = math.sin(self.pos.x / 20) * 20  # Oscillation en y

    def move_linear(self):
        if self.pos.x > POS_GAME_X_END - self.rect.width:
            self.speed *= -1
        if self.pos.x < POS_GAME_X_BEGAN:
            self.speed *= -1
        
        self.pos.x += self.speed *self.game.dt * 50


    def move_stationary(self):
        pass

    def set_pattern(self, pattern):
        self.pattern = pattern
        

    def update(self):
        # Appeler le pattern de déplacement approprié
        if self.pattern == "circle":
            self.move_circle()
        elif self.pattern == "zigzag":
            self.move_zigzag()
        elif self.pattern == "linear":
            self.move_linear()
        elif self.pattern == "stationary":
            self.move_stationary()

        self.shoot()

        self.rect.center = self.pos