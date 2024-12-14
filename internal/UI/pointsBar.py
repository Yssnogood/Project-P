import pygame as pg
from internal.game.settings import *

class PointsBar:
    def __init__(self, game, player, x, y,  radius=20, spacing=5):
        self.game = game
        self.x = x
        self.y = y
        self.player = player
        self.radius = radius
        self.spacing = spacing


    def draw(self):

        for i in range(self.player.max_health):
            circle_x = self.x + i * (2 * self.radius + self.spacing)
            pg.draw.circle(self.game.screen, BLACK, (circle_x, self.y), self.radius)
        for i in range(self.player.health):
            circle_x = self.x + i * (2 * self.radius + self.spacing)
            pg.draw.circle(self.game.screen, YELLOW, (circle_x, self.y), self.radius)

        for i in range(self.player.maxBom):
            circle_x = self.x + i * (2 * self.radius + self.spacing)
            pg.draw.circle(self.game.screen, BLACK, (circle_x, self.y + (2*self.radius + self.spacing) ), self.radius)
        for i in range(self.player.bombCounter):
            circle_x = self.x + i * (2 * self.radius + self.spacing)
            pg.draw.circle(self.game.screen, ORANGE, (circle_x, self.y + (2*self.radius + self.spacing)), self.radius)