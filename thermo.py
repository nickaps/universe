import Universe as cosmos
import pygame as pg
import random


SPACETIME = cosmos.Spacetime()

SPACETIME.G = 0
SPACETIME.tickrate = 0.0000000001
SPACETIME.rC = 0.01
SPACETIME.electroC = 0.01

C=5

for x in range(C):
        cosmos.Particle(random.randint(100,1300),
                        random.randint(100,700),
                        SPACETIME,
                        0,
                        0,
                        100,
                        1000,
                        4300,
                        0.1,
                        0.5,
                        1)
for x in range(C):
        cosmos.Particle(random.randint(100,1300),
                    random.randint(100,700),
                    SPACETIME,
                    0,
                    0,
                    1,
                    1,
                    1000,
                    0.1,
                    0.1,
                    -1)

loop = True
while loop is True:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        pg.display.quit()
                        pg.quit()
        SPACETIME.time()
        pg.display.update()