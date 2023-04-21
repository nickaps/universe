import Universe as cosmos
import pygame as pg


SPACETIME = cosmos.Spacetime()

SPACETIME.G_down = 0.000
SPACETIME.tickrate = 0.1
SPACETIME.electroC = 500


P1 = cosmos.Particle(650,
                    700,
                    SPACETIME,
                    100,
                    0,
                    100,
                    100,
                    4400,
                    0.1,
                    0.25,-1)

P2 = cosmos.Particle(650,
                    100,
                    SPACETIME,
                    -100,
                    0,
                    100,
                    100,
                    1000,
                    0.1,
                    0.25,1)

loop = True
while loop is True:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        pg.display.quit()
                        pg.quit()
        SPACETIME.time()
        pg.display.update()