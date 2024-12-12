import pygame as pg
import math
from internal.entities.ennemies.ennemiesProjectile import *
from internal.game.settings import *

vec = pg.math.Vector2

class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_bosses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Appearance
        self.image = pg.Surface((50, 75), pg.SRCALPHA)  # Large boss sprite
        pg.draw.ellipse(self.image, YELLOW, (0, 0, 100, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 

        # Position and movement
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.speed = 2

        # Stats
        self.health = 300

        # Attack patterns
        self.attack_delay = 2000  # Milliseconds between attacks
        self.last_attack_time = 0

        # Phases
        self.current_phase = "first"
        self.phase_health_thresholds = {
            "second": 200,
            "third": 100
        }

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            print("Boss defeated!")

    def change_phase(self):
        if self.current_phase == "first" and self.health <= self.phase_health_thresholds["second"]:
            self.current_phase = "second"
            print("Boss enters second phase!")
        elif self.current_phase == "second" and self.health <= self.phase_health_thresholds["third"]:
            self.current_phase = "third"
            print("Boss enters third phase!")

    def shoot_circle(self, num_projectiles=12):
        """Shoots projectiles in a circle."""
        angle_step = 2 * math.pi / num_projectiles
        now = pg.time.get_ticks()
        if now - self.last_attack_time > self.attack_delay:
            self.last_attack_time = now
            for i in range(num_projectiles):
                angle = i * angle_step
                direction = vec(math.cos(angle), math.sin(angle))
                EnemyProjectile(self.game, self.rect.centerx, self.rect.centery, direction)

    def move(self):
        """Simple back-and-forth movement."""
        if self.rect.right >= POS_GAME_X_END -50 or self.rect.left <= POS_GAME_X_BEGAN:
            self.vel.x *= -1
        self.pos += self.vel * self.speed + (0.5,0)

        # Update position on screen
        self.rect.center = self.pos

    def update(self):
        self.move()
