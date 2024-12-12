from internal.triggers.triggerFairiesSpawn import *
from internal.entities.ennemies.boss import *

class Orchestrator:
    def __init__(self, game):
        self.game = game
        self.fairies = FairiesSpawn(self.game)

        self.waves = {
            "first":False,
            "second":False
        }


        self.last_spawn_time = 0  # Enregistre le moment du dernier spawn
        self.spawn_interval = 5000  # Temps entre les apparitions (en millisecondes)

    def spawnBoss(self):
        self.boss = Boss(self.game, WIDTH//2, 100)
        


    def firstFairies(self):
        self.fairies.spawnFairy(POS_GAME_X_BEGAN + 30, 70,FAIRY_PATERN[-1],10,200,"circle")
        self.fairies.spawnFairy(POS_GAME_X_END - 80, 70,FAIRY_PATERN[-1],10,200,"circle")
        self.fairies.spawnFairy(WIDTH//2,70,FAIRY_PATERN[-1],10,200,"circle")


    def fairiesFirstWave(self):
        now = pg.time.get_ticks()  # Temps actuel en millisecondes
        if now - self.last_spawn_time > self.spawn_interval and not self.waves["first"]:
            self.waves["first"] = True
            self.last_spawn_time = now  # Met à jour le dernier moment de spawn
            self.fairies.spawnFairiesLine(5, POS_GAME_X_BEGAN+50,200, FAIRY_PATERN[0])

            self.fairies.spawnFairy(WIDTH//2 +60,140,FAIRY_PATERN[-1],10,200,"circle")
            self.fairies.spawnFairy(WIDTH//2 -60,140,FAIRY_PATERN[-1],10,200,"circle")

        if now - self.last_spawn_time > self.spawn_interval + 3000  and not self.waves["second"]:
            self.last_spawn_time = now  # Met à jour le dernier moment de spawn
            self.waves["second"] = True
            
            self.fairies.spawnFairy(WIDTH//2,70,FAIRY_PATERN[-1],10,200,"circle")
            self.fairies.spawnFairiesLine(5, POS_GAME_X_BEGAN+50,200, FAIRY_PATERN[0])
            self.fairies.spawnFairiesColumn(2, POS_GAME_X_BEGAN + 30, 40,FAIRY_PATERN[-1])
            self.fairies.spawnFairiesColumn(2, POS_GAME_X_END - 80, 40,FAIRY_PATERN[-1])




