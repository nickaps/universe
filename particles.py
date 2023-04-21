import Universe as cosmos
import pygame as pg
import random


SPACETIME = cosmos.Spacetime()

SPACETIME.G_down = 1
SPACETIME.tickrate = 0.5
SPACETIME.rC = 0.0004
SPACETIME.electroC = 300


pcount = 50
for p in range(pcount):
        cosmos.Particle(random.randint(100,1300),
                    random.randint(100,700),
                    SPACETIME,
                    random.randint(-100,100)/200,
                    random.randint(-100,100)/200,
                    100,                                        #100/10 = 10 m/a
                    10,
                    random.randint(500,5000),
                    0.1,
                    0.3,
                    random.randint(-1,1))

loop = True
while loop is True:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        pg.display.quit()
                        pg.quit()
        SPACETIME.time()
        pg.display.update()