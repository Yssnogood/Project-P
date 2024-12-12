from internal.entities.ennemies.fairy import *
import random

class FairiesSpawn:
    def __init__(self, game):
        self.game = game

    def spawnFairy(self, x ,y, patern=FAIRY_PATERN[-1],speed=10, radius=200, shoot_patern="linear",pattern_params=None):
        self.fairy = Fairy(self.game, x, y,patern,speed,radius,shoot_patern, pattern_params)
        self.game.all_sprites.add(self.fairy)
        self.game.all_fairy.add(self.fairy)

    def spawnFairies(self, amount):
        for i in range(amount):
            self.fairy = Fairy(self.game, random.randint(POS_GAME_X_BEGAN,POS_GAME_X_END - 60), random.randint(50,300), FAIRY_PATERN[0], -5)
            self.game.all_sprites.add(self.fairy)
            self.game.all_fairy.add(self.fairy)

    def spawnFairiesLine(self, amount, startSpawnX=POS_GAME_X_BEGAN, startSpawnY=0, patern=FAIRY_PATERN[-1]):

        if startSpawnX <POS_GAME_X_BEGAN or startSpawnX > POS_GAME_X_END:
            startSpawnX = POS_GAME_X_BEGAN + FAIRY_SIZE
        else :
            startSpawnX = startSpawnX + FAIRY_SIZE

        if startSpawnY == 0 or startSpawnY > HEIGHT//2:
            startSpawnY =  random.randint(50,300)

        for i in range(amount):
            self.fairy = Fairy(self.game, startSpawnX, startSpawnY, patern, -5)
            self.game.all_sprites.add(self.fairy)
            self.game.all_fairy.add(self.fairy)
            startSpawnX = startSpawnX + FAIRY_SIZE + 45 

    def spawnFairiesColumn(self, amount, startSpawnX=0, startSpawnY=30, patern=FAIRY_PATERN[-1], shoot_patern="linear"):

        if startSpawnY < 30 or startSpawnY > HEIGHT//2:
            startSpawnY = 10 + FAIRY_SIZE
        
        if startSpawnX == 0:
            startSpawnX = random.randint(POS_GAME_X_BEGAN,POS_GAME_X_END)
            
        for i in range(amount):
            self.fairy = Fairy(self.game, startSpawnX, startSpawnY, patern, 10,200,shoot_patern)
            self.game.all_sprites.add(self.fairy)
            self.game.all_fairy.add(self.fairy)
            startSpawnY = startSpawnY + FAIRY_SIZE + 50 
    