import pygame as pg
import math
from internal.entities.ennemies.ennemiesProjectile import *
from internal.entities.ennemies.megaEnnemiesProjectile import *
from internal.game.settings import *

vec = pg.math.Vector2

class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_bosses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Appearance
        self.image = pg.Surface((75, 50))  # Large boss sprite
        #pg.draw.ellipse(self.image, YELLOW, (0, 0, 100, 150))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 

        # Position and movement
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.speed = 5

        # Stats
        self.health = 500

        # Attack patterns
        self.attack_delay = 500  # Milliseconds between attacks
        self.last_attack_time = 0

        # Phases
        self.current_phase = "first"

        self.phase = {
            "first":True,
            "second":False,
            "third":False
        }

        self.phase_health_thresholds = {
            "second": 300,
            "third": 130
        }

    def first_phase(self):

        self.shoot_megaProjectile()
        self.shoot_megaProjectile(POS_GAME_X_END-60)

        self.shoot_megaProjectile(POS_GAME_X_BEGAN + 20, HEIGHT // 3)
        self.shoot_megaProjectile(POS_GAME_X_END - 60, HEIGHT // 3)
        
        
        self.shoot_megaProjectile(WIDTH//2 -30, HEIGHT // 4, "linear")
        self.shoot_megaProjectile(WIDTH//2 +30, HEIGHT // 4, "linear")

    def second_phase(self):
        for project in self.game.ennemies_mega_projectiles:
            project.kill()
        for project in self.game.ennemies_projectiles:
            project.kill()

        self.shoot_megaProjectile(POS_GAME_X_BEGAN + 20, HEIGHT // 4, "linear")
        self.shoot_megaProjectile(POS_GAME_X_END - 60, HEIGHT // 4, "linear")

        self.shoot_megaProjectile(POS_GAME_X_BEGAN + 40, HEIGHT // 4 + 50, "circle")
        self.shoot_megaProjectile(POS_GAME_X_END - 80, HEIGHT // 4+ 50, "circle")

        self.shoot_megaProjectile(WIDTH//2 -50, HEIGHT // 5, "star")
        self.shoot_megaProjectile(WIDTH//2 +50, HEIGHT // 5, "star")

    def third_phase(self):
        for project in self.game.ennemies_mega_projectiles:
            project.kill()
        for project in self.game.ennemies_projectiles:
            project.kill()
            
        self.shoot_megaProjectile(WIDTH//2 -30, HEIGHT // 4, "linear")
        self.shoot_megaProjectile(WIDTH//2 +30, HEIGHT // 4, "linear")
        

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            for project in self.game.ennemies_mega_projectiles:
                project.kill()
            for project in self.game.ennemies_projectiles:
                project.kill()
            print("Boss defeated!")

    def change_phase(self):
        if self.current_phase == "first" and self.health <= self.phase_health_thresholds["second"]:
            self.current_phase = "second"
            self.phase["second"] = True
            self.image.fill(YELLOW)
            print("Boss enters second phase!")
        elif self.current_phase == "second" and self.health <= self.phase_health_thresholds["third"]:
            self.current_phase = "third"
            self.phase["third"] = True
            self.image.fill(ORANGE)
            print("Boss enters third phase!")
    
    def boss_fight(self):
        if self.current_phase == "first" and self.phase["first"]:
            self.phase["first"] = False
            self.first_phase()
        elif self.current_phase == "second" and self.phase["second"]:
            self.phase["second"] = False
            self.second_phase()
        elif self.current_phase == "third" and self.phase["third"]:
            self.phase["third"] = False
            self.third_phase()

    def shoot_megaProjectile(self, x=POS_GAME_X_BEGAN + 20, y = 120, shoot_patern="star"):
        angle = 2 * math.pi
        direction = vec(math.cos(angle), math.sin(angle))
        EnemyMegaProjectile(self.game, self.pos.x, self.pos.y, direction, x, y, shoot_patern )


    def shoot(self, num_projectiles=12):
        """Shoots projectiles in a circle."""
        angle_step = 2 * math.pi / num_projectiles
        now = pg.time.get_ticks()
        if now - self.last_attack_time > self.attack_delay:
            self.last_attack_time = now
            for i in range(num_projectiles):
                angle = i * angle_step
                direction = vec(math.cos(angle), math.sin(angle))
                EnemyProjectile(self.game, self.rect.centerx, self.rect.centery, direction)
            if self.current_phase == "second" or self.current_phase == "third":
                player_pos = vec(self.game.player.rect.center)
                direction = (player_pos - self.pos).normalize()

                EnemyProjectile(self.game, self.rect.left, self.rect.y, direction)
                EnemyProjectile(self.game, self.rect.right-10, self.rect.y, direction)
            if self.current_phase == "third":
                num_branches=9
                spread_angle=0.2
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

    def move(self):
        """Simple back-and-forth movement."""
        if self.pos.x > POS_GAME_X_END - self.rect.width or self.pos.x < POS_GAME_X_BEGAN:
            self.speed *= -1
        self.pos.x +=  self.speed * self.game.dt * 50

        # Update position on screen
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self):
        self.change_phase()
        self.boss_fight()
        self.move()
        self.shoot()
