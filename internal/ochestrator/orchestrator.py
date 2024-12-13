from internal.triggers.triggerFairiesSpawn import *
from internal.entities.ennemies.boss import *

class Orchestrator:
    def __init__(self, game):
        self.game = game
        self.fairies = FairiesSpawn(self.game)

        self.waves = {
            "first":False,
            "second":False,
            "third":False
        }


        self.last_spawn_time = 0  # Enregistre le moment du dernier spawn
        self.spawn_interval = 5000  # Temps entre les apparitions (en millisecondes)

    def spawnBoss(self):
        self.boss = Boss(self.game, WIDTH//2, 100)
        #self.boss.second_phase()

    def firstFairies(self):
        self.fairies.spawnFairy(POS_GAME_X_BEGAN + 30, 70,FAIRY_PATERN[-1],10,200,"circle",None,ROSYBROWN)
        self.fairies.spawnFairy(POS_GAME_X_END - 80, 70,FAIRY_PATERN[-1],10,200,"circle",None,ROSYBROWN)
        self.fairies.spawnFairy(WIDTH//2,70,FAIRY_PATERN[-1],10,200,"circle",None,ROSYBROWN)


    def fairiesFirstWave(self):
        now = pg.time.get_ticks()  # Temps actuel en millisecondes
        if now - self.last_spawn_time > self.spawn_interval and not self.waves["first"]:
            self.waves["first"] = True
            self.last_spawn_time = now  # Met à jour le dernier moment de spawn
            self.fairies.spawnFairiesLine(5, POS_GAME_X_BEGAN+50,200, FAIRY_PATERN[0],PURPLE )

            self.fairies.spawnFairy(WIDTH//2 +60,140,FAIRY_PATERN[-1],10,200,"circle",None,PURPLE)
            self.fairies.spawnFairy(WIDTH//2 -60,140,FAIRY_PATERN[-1],10,200,"circle",None,PURPLE)

        if now - self.last_spawn_time > self.spawn_interval + 5000  and not self.waves["second"]:
            for fairy in self.game.all_fairy:
                fairy.kill()

            self.last_spawn_time = now  # Met à jour le dernier moment de spawn
            self.waves["second"] = True
            
            self.fairies.spawnFairy(WIDTH//2,70,FAIRY_PATERN[-1],10,200,"circle",None, LIGHTSKYBLUE)
            self.fairies.spawnFairiesLine(5, POS_GAME_X_BEGAN+50,200, FAIRY_PATERN[0],LIGHTSKYBLUE)
            self.fairies.spawnFairiesColumn(2, POS_GAME_X_BEGAN + 30, 40,FAIRY_PATERN[-1], LIGHTSKYBLUE)
            self.fairies.spawnFairiesColumn(2, POS_GAME_X_END - 80, 40,FAIRY_PATERN[-1], LIGHTSKYBLUE)

        if now - self.last_spawn_time > self.spawn_interval + 5000 and not self.waves["third"]:
            
            for fairy in self.game.all_fairy:
                fairy.kill()
            
            if now - self.last_spawn_time > self.spawn_interval + 10000:
                self.last_spawn_time = now  # Met à jour le dernier moment de spawn
                self.waves["third"] = True
                self.spawnBoss() 


