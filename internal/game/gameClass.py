import pygame as pg
import sys

from os import path
from internal.entities import player, fairy
from internal.game.settings import *

class Game:
    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.game_space = pg.Surface((WIDTH//2, HEIGHT))
        self.game_space.fill(BLACK)
        
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)

    def new(self):
        # initialize all variables and do all the se    tup for a new game
        self.all_sprites = pg.sprite.Group()
        self.all_fairy = pg.sprite.Group()
        self.player = player.Player(self, pg.Surface.get_width(self.game_space)//1 , HEIGHT//1.25)
        self.testo = fairy.Fairy(self,  pg.Surface.get_width(self.game_space)//1 , HEIGHT//1.50)
        self.all_sprites.add(self.testo)
        self.all_fairy.add(self.testo)

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
        hits = pg.sprite.spritecollide(self.player, self.all_fairy, True)
        if hits:
            print("szr")
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
