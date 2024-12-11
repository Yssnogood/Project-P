import sys
import os

from internal.game import gameClass

# create the game object
g = gameClass.Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
