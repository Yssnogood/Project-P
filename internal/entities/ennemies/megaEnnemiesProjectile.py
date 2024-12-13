import pygame as pg
import math
from internal.game.settings import *
from internal.entities.ennemies.ennemiesProjectile import *

vec = pg.math.Vector2


class EnemyMegaProjectile(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction, xFinal, yFinal, shoot_parttern="star"):
        self.groups = game.all_sprites, game.ennemies_mega_projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.health = 150

        # Create projectile image
        self.radius = 20
        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, BLUE, (self.radius, self.radius), self.radius)
        self.rect = pg.Rect(0, 0, self.radius * 2, self.radius)
        self.rect.center = (x, y)

        self.pos = vec(x, y)
        self.vel = vec(0, 0)  # No initial velocity
        self.direction = direction

        self.damage = 1

        self.shoot_pattern = shoot_parttern

        self.shoot_patterns = {
            "circle": self.shoot_circle,
            "star":self.shoot_star,
            "linear": self.shoot,
            "straight":self.shoot_straight
        }

        # Target position
        self.target_pos = vec(xFinal, yFinal)
        self.reached_target = False
        self.speed = 100  # Speed of movement towards the final position

        # Shooting pattern
        self.shoot_delay = 1000  # Time between shots in milliseconds
        self.last_shot_time = 0

        # Rotation
        self.rotation_angle = 0  # Current rotation angle in degrees
        self.rotation_speed = 180  # Degrees per second

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            print("MegaProjectile have been destroyed")

    def moveToFinalPosition(self):
        """Moves the projectile towards its final position."""
        if not self.reached_target:
            direction_to_target = (self.target_pos - self.pos).normalize()
            distance_to_target = self.target_pos.distance_to(self.pos)

            # Move closer to the target
            if distance_to_target > 5:  # Threshold to consider the target reached
                self.vel = direction_to_target * self.speed * self.game.dt
                self.pos += self.vel
            else:
                self.reached_target = True
                self.vel = vec(0, 0)  # Stop moving

    def shoot(self):
        # Calculate direction towards the player
        player_pos = vec(self.game.player.rect.center)
        direction = (player_pos - self.pos).normalize()

        now = pg.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            EnemyProjectile(self.game, self.rect.left, self.rect.y, direction)
            EnemyProjectile(self.game, self.rect.right-10, self.rect.y, direction)

    def shoot_straight(self, vecX=0, vecY=1):
        now = pg.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            direction = vec(vecX,vecY).normalize()
            EnemyProjectile(self.game, self.rect.left, self.rect.y, direction)
            EnemyProjectile(self.game, self.rect.right-10, self.rect.y, direction)

    def shoot_circle(self, num_projectiles=16):
        """Shoots projectiles in a circular pattern."""
        if self.reached_target:
            now = pg.time.get_ticks()
            if now - self.last_shot_time > self.shoot_delay:
                self.last_shot_time = now
                angle_step = 2 * math.pi / num_projectiles
                for i in range(num_projectiles):
                    angle = i * angle_step
                    direction = vec(math.cos(angle), math.sin(angle))
                    EnemyProjectile(self.game, self.rect.centerx, self.rect.centery, direction)
                

    def shoot_star(self, num_branches=9, spread_angle=0.2):
        if self.reached_target:
            now = pg.time.get_ticks()
            if now - self.last_shot_time > self.shoot_delay:
                self.last_shot_time = now
                angle_step = 2 * math.pi / num_branches
                for i in range(num_branches):
                    base_angle = i * angle_step
                    # Two projectiles per branch, slightly diverging
                    angle1 = base_angle - spread_angle / 2
                    angle2 = base_angle + spread_angle / 2
                    direction1 = vec(math.cos(angle1), math.sin(angle1))
                    direction2 = vec(math.cos(angle2), math.sin(angle2))
                    # Create the two projectiles
                    EnemyProjectile(self.game, self.rect.centerx, self.rect.centery, direction1)
                    EnemyProjectile(self.game, self.rect.centerx, self.rect.centery, direction2)
 
    def update(self):
        """Updates the position and handles shooting."""
        if not self.reached_target:
            self.moveToFinalPosition()
        else:
            # Call the appropriate shooting pattern
            shoot_function = self.shoot_patterns.get(self.shoot_pattern, self.shoot_circle)
            shoot_function()
        # Update the sprite's position on screen
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
