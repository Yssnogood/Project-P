import pygame as pg
from internal.game.settings import *
from internal.entities.ennemies.ennemiesProjectile import *
import math

vec = pg.math.Vector2

class Fairy(pg.sprite.Sprite):
    def __init__(self, game, x, y, pattern="zigzag", speed=10, radius=200, shoot_pattern="linear",  pattern_params=None,color=(0,255,0)):
        self.groups = game.all_sprites, game.all_fairy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        # Create and center the image
        self.image = pg.Surface((FAIRY_SIZE, FAIRY_SIZE), pg.SRCALPHA)
        self.color = color
        pg.draw.circle(self.image, self.color, (FAIRY_SIZE // 2, FAIRY_SIZE // 2), FAIRY_SIZE // 2)
        self.rect = self.image.get_rect(center=(x, y))

        # Initialize movement and shooting variables
        self.pos = vec(x, y)
        self.center = vec(x, y)  # Center for circular movements
        self.angle = 0           # Angle for circular patterns
        self.radius = radius
        self.speed = speed
        self.direction = vec(1, 0)  # Direction for linear movement

        self.last_shot_time = 0
        self.shoot_delay = 500
        self.shoot_pattern = shoot_pattern

        self.health = 30

        # Movement patterns
        self.pattern = pattern
        self.pattern_params = pattern_params or {}
        self.patterns = {
            "circle": self.move_circle,
            "zigzag": self.move_zigzag,
            "linear": self.move_linear,
            "stationary": self.move_stationary
        }

        # Shooting patterns
        self.shoot_patterns = {
            "circle": self.shoot_circle,
            "linear": self.shoot
        }

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            print("A fairy has been killed")

    def shoot(self):
        # Calculate direction towards the player
        player_pos = vec(self.game.player.rect.center)
        direction = (player_pos - self.pos).normalize()

        now = pg.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            EnemyProjectile(self.game, self.pos.x, self.pos.y, direction)

    def shoot_circle(self, num_projectiles=12):
        angle_step = 2 * math.pi / num_projectiles

        now = pg.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now

            for i in range(num_projectiles):
                angle = i * angle_step
                direction = vec(math.cos(angle), math.sin(angle))
                EnemyProjectile(self.game, self.pos.x, self.pos.y, direction)

    # Movement patterns
    def move_circle(self):
        self.angle += self.speed * self.game.dt
        self.angle %= 2 * math.pi
        self.pos.x = self.center.x + self.radius * math.cos(self.angle)
        self.pos.y = self.center.y + self.radius * math.sin(self.angle)

    def move_zigzag(self):
        amplitude = self.pattern_params.get("amplitude", 20)
        frequency = self.pattern_params.get("frequency", 20)

        if self.pos.x > POS_GAME_X_END - self.rect.width or self.pos.x < POS_GAME_X_BEGAN:
            self.speed *= -1

        self.pos.x += self.speed * self.game.dt * 50
        self.pos.y += math.sin(self.pos.x / frequency) * amplitude

    def move_linear(self):
        if self.pos.x > POS_GAME_X_END - self.rect.width or self.pos.x < POS_GAME_X_BEGAN:
            self.speed *= -1
        self.pos.x += self.speed * self.game.dt * 50

    def move_stationary(self):
        pass

    def set_pattern(self, pattern, pattern_params=None):
        self.pattern = pattern
        if pattern_params:
            self.pattern_params = pattern_params

    def update(self):
        # Call the appropriate movement pattern
        move_function = self.patterns.get(self.pattern, self.move_stationary)
        move_function()

        # Synchronize the rect's position
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        # Call the appropriate shooting pattern
        shoot_function = self.shoot_patterns.get(self.shoot_pattern, self.shoot)
        shoot_function()