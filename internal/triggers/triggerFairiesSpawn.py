from internal.entities.ennemies.fairy import *
import random

class FairiesSpawn:
    def __init__(self, game):
        self.game = game

    def spawnFairies(self, amount):
        for i in range(amount):
            self.fairy = Fairy(self.game, random.randint(POS_GAME_X_BEGAN,POS_GAME_X_END - 60), random.randint(50,300), FAIRY_PATERN[0], -5)
            self.game.all_sprites.add(self.fairy)
            self.game.all_fairy.add(self.fairy)

    def spawnFairiesLine(self, amount):
        startSpawnX = POS_GAME_X_BEGAN + FAIRY_SIZE
        startSpawnY =  random.randint(50,300)
        for i in range(amount):
            self.fairy = Fairy(self.game, startSpawnX, startSpawnY, FAIRY_PATERN[-1], -5)
            self.game.all_sprites.add(self.fairy)
            self.game.all_fairy.add(self.fairy)
            startSpawnX = startSpawnX + FAIRY_SIZE + 30 

    def spawnFairiesColumn(self, amount, startSpawnX=0):
        startSpawnY = 10 + FAIRY_SIZE
        if startSpawnX == 0:
            startSpawnX =   random.randint(POS_GAME_X_BEGAN,POS_GAME_X_END)
            
        for i in range(amount):
            self.fairy = Fairy(self.game, startSpawnX, startSpawnY, FAIRY_PATERN[-1], -5)
            self.game.all_sprites.add(self.fairy)
            self.game.all_fairy.add(self.fairy)
            startSpawnY = startSpawnY + FAIRY_SIZE + 30 
    