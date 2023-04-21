import Universe as cosmos
import pygame as pg


SPACETIME = cosmos.Spacetime()

SPACETIME.G_down = 0.000
SPACETIME.G = 0.01
SPACETIME.tickrate =5
SPACETIME.heatJitter = 0

P2 = cosmos.Particle(650,
                    400,
                    SPACETIME,
                    0,
                    0,
                    10000000,
                    10000,
                    6000,
                    0.1, 2, 0)

P1 = cosmos.Particle(650,
                    750,
                    SPACETIME,
                    45,
                    0,
                    1000,
                    100,
                    0,
                    0.1,
                    0.3,0)

P1 = cosmos.Particle(650,
                    500,
                    SPACETIME,
                    30,
                    0,
                    1000,
                    1000,
                    1900,
                    0.1,
                    0.3,0)



loop = True
while loop is True:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        pg.display.quit()
                        pg.quit()
        SPACETIME.time()
        pg.display.update()