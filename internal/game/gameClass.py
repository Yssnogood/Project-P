import pygame as pg
import sys

from os import path
from internal.entities.player import player
from internal.entities.ennemies import fairy
from internal.game.settings import *
from internal.triggers.triggerFairiesSpawn import *

class Game:
    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.game_space = pg.Surface((WIDTH//2, HEIGHT))
        self.game_space.fill(BLACK)
        
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

        self.trigger = FairiesSpawn(self)

    def load_data(self):
        game_folder = path.dirname(__file__)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.all_fairy = pg.sprite.Group()
        self.player_projectiles = pg.sprite.Group()
        self.ennemies_projectiles = pg.sprite.Group()

        self.player = player.Player(self, pg.Surface.get_width(self.game_space)//1 , HEIGHT//1.25)
        self.testo = fairy.Fairy(self, 600, 200, "circle")

        self.all_sprites.add(self.testo)
        self.all_fairy.add(self.testo)

        self.trigger.spawnFairies(3)
        self.trigger.spawnFairiesLine(5)
        self.trigger.spawnFairiesColumn(3, POS_GAME_X_BEGAN + 30)
        self.trigger.spawnFairiesColumn(3, POS_GAME_X_END - 80)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        # Vérifie les collisions entre les projectiles et les ennemis
        for projectile in self.player_projectiles:
            fairy_hit = pg.sprite.spritecollide(projectile, self.all_fairy, False) # Collisions avec les ennemis
            for fairy in fairy_hit:
                fairy.take_domage(projectile.domage)
                projectile.kill() 
        for projectile in self.ennemies_projectiles:
            if self.player.rect.colliderect(projectile.rect):  # Utilisation de colliderect pour un seul joueur
                self.player.take_domage(projectile.domage)
                projectile.kill()


    def draw(self):
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.game_space,(POS_GAME_X_BEGAN,HEIGHT*0))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image,sprite.pos)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
