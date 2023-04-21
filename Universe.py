import random
import math
import numpy as np
import pygame as pg
import time


T = 0.0001
bT = 0

loop = True

pg.init()
win = pg.display.set_mode((1400,800))
pg.display.set_caption('Universe')

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

#interface for mass and energy
class Spacetime:
        def __init__ (self, G=0.00001, down=0.0000, b=bT, tick=T):
                self.buffer = b
                self.win = win
                self.particles = []
                self.tickrate = tick
                self.clock = 0
                self.G = G
                self.G_down = down
                self.rC = 0.00001
                self.energySpread = 0.05
                self.bounceRegulator = 0.1
                self.massTransfer = 0.1
                self.heatJitter = 0.01
                self.wC = 5000
                self.dimC = 100
                self.electroC = 5
                self.nuclearC = 0.0001
        def time (self):
                self.win.fill((0,0,4))
                self.clock += self.tickrate
                for particle in self.particles:
                        particle.radiate()
                for particle in self.particles:
                        particle.behave(self.tickrate)
                        particle.collision()
                        particle.electro()
                        particle.nuclear()
                time.sleep(self.buffer)

def energy_color_scale(E,wC):
        if E < wC:
                b = max(0, min(max(0,int(np.round(-(((E-1595)/100)**2)+255))) + max(0,int(np.round(-(((E-5000)/40)**2)+255))), 255))
                g = max(0, min(max(0,int(np.round(-(((E-3000)/100)**2)+255))) + max(0,int(np.round(-(((E-5000)/40)**2)+255))), 255))
                r = max(0, min(int(np.round(-(((E-5000)/100)**2)+255)), 255))
                return r,g,b
        else:
                return 255,255,255

class Particle:
        def __init__(self, x, y, spacetime, dx=0, dy=0, mass=1, area=1, energy=1, friction=0.001, lum=1, charge=0):
                self.spacetime = spacetime
                self.spacetime.particles.append(self)
                self.x = x
                self.y = y
                self.posf = (self.x,self.y)
                self.pos = (int(np.round(self.x)),int(np.round(self.y)))
                self.dx = dx
                self.dy = dy
                self.v = (self.dx,self.dy)
                self.tV = (self.dx+self.dy)/2
                self.mass = mass
                self.area = area
                self.radiusf = np.sqrt(area/np.pi)
                self.radius = int(np.round(np.sqrt(area/np.pi)))
                self.friction = friction
                self.px = self.mass * self.dx
                self.py = self.mass * self.dy
                self.density = self.mass/self.area
                self.radiation_radius = 0
                self.energy = energy
                self.radiation = 0
                self.r, self.g, self.b = energy_color_scale(self.energy, self.spacetime.wC)
                self.color = (self.r, self.g, max(self.b, 4))
                self.lum = lum
                self.radcolor = (max(max(0, self.r-self.spacetime.dimC), 255), max(max(0, self.g-self.spacetime.dimC), 255), max(max(0, self.b-self.spacetime.dimC), 255))
                self.collisions = []
                self.charge = int(np.round(charge))

        def direction(self):
                if self.dx == 0 and self.dy == 0:
                        return None
                elif self.dx != 0 and self.dy > 0:
                        return np.abs(np.arctan(self.dy/self.dx))
                elif self.dx != 0 and self.dy < 0:
                        return -np.abs(np.arctan(self.dy/self.dx))

        def recolor(self):
                self.r, self.g, self.b = energy_color_scale(self.energy, self.spacetime.wC)
                self.color = (self.r, self.g, self.b)
                self.radcolor = (max(0, self.r-self.spacetime.dimC*(np.sin((self.spacetime.clock*self.spacetime.tickrate)*self.charge/np.pi)+1)), 
                                 max(0, self.g-self.spacetime.dimC*(np.sin((self.spacetime.clock*self.spacetime.tickrate)*self.charge/np.pi)+1)),
                                 max(0, self.b-self.spacetime.dimC*(np.sin((self.spacetime.clock*self.spacetime.tickrate)*self.charge/np.pi)+1)))

        def setpos(self, newpos):
                self.pos = newpos
        
        def velocity(self):
                self.px = self.mass * self.dx
                self.py = self.mass * self.dy
                self.x += np.nan_to_num((self.dx*self.spacetime.tickrate + ((random.randrange(-100,100)/100)*self.energy*self.spacetime.heatJitter))/self.mass)
                self.y -= np.nan_to_num((self.dy*self.spacetime.tickrate + ((random.randrange(-100,100)/100)*self.energy*self.spacetime.heatJitter))/self.mass)
                self.posf = (self.x,self.y)
                x, y = int(math.trunc(self.x)), int(math.trunc(self.y))
                self.setpos((x,y))

        def pDistance(self, _point2):
                x1, x2 = self.x, _point2[0]
                y1, y2 = self.y, _point2[1]
                d = np.sqrt((x2-x1)**2+(y2-y1)**2)
                return d

        def distance(self, _mass2):
                x1, x2 = self.x, _mass2.x
                y1, y2 = self.y, _mass2.y
                d = np.sqrt((x2-x1)**2+(y2-y1)**2)
                return d

        def burst(self,burst=1):
                for particle in self.spacetime.particles:
                        if particle is not self and particle not in self.collisions:
                                particle.force((particle.x-self.x, particle.y-self.y), burst/self.distance(particle)*self.spacetime.tickrate)

        def gravity(self):
                self.dy -= self.spacetime.G_down
                if len(self.spacetime.particles) > 1:
                        for particle in self.spacetime.particles:
                                if particle is not self and particle not in self.collisions:
                                        self.force((particle.x, particle.y), ((particle.density)/self.distance(particle)*self.spacetime.tickrate*self.spacetime.G))

        def electro(self):
                if len(self.spacetime.particles) > 1:
                        for particle in self.spacetime.particles:
                                if self.charge == 0:
                                        return None
                                elif particle is not self and particle not in self.collisions and (self.charge + particle.charge) == 0:
                                        self.force((particle.x, particle.y), self.spacetime.electroC/self.distance(particle)*self.spacetime.tickrate)
                                elif particle is not self and particle not in self.collisions and np.abs(self.charge + particle.charge) == 2:
                                        self.force((particle.x, particle.y), -self.spacetime.electroC/self.distance(particle)*self.spacetime.tickrate)

        def nuclear(self):
                if len(self.spacetime.particles) > 1:
                        for particle in self.spacetime.particles:
                                if particle.charge == self.charge and particle in self.collisions:
                                        self.burst(self.spacetime.nuclearC)
                                        self.force((particle.x, particle.y), self.spacetime.nuclearC)



        def radiate(self):
                if self.energy > 0:
                        radiation_constant = self.spacetime.rC
                        self.radiation = self.energy * radiation_constant
                        self.radiation_radius = self.energy*self.spacetime.energySpread*self.lum
                        self.energy -= self.radiation*self.spacetime.tickrate
                        draw_circle_alpha(win, self.radcolor, (int(np.round(self.x)), int(np.round(self.y))), int(np.round(self.radiation_radius)))
                        if len(self.spacetime.particles) > 1:
                                for particle in self.spacetime.particles:
                                        if particle is not self and self.distance(particle) <= self.radiation_radius:
                                                particle.energy += max(0, (self.radiation/particle.area))*(self.energy-particle.energy)/(self.distance(particle)*self.radiation)

        def collision(self):
                self.collisions = []

                if self.x >= 1400-self.radius:
                        self.x = 1400-self.radius
                        self.dx *= -1 + self.friction
                if self.x < self.radius:
                        self.x = self.radius
                        self.dx *= -1 + self.friction
                if self.y >= 800-self.radius:
                        self.y = 800-self.radius
                        self.dy *= -1 + self.friction
                if self.y < self.radius:
                        self.y = self.radius
                        self.dy *= -1 + self.friction
                

                if len(self.spacetime.particles) > 1:
                        for particle in self.spacetime.particles:
                                if particle is not self:
                                        if self.distance(particle) <= self.radiusf + particle.radiusf:
                                                self.collisions.append(particle)
                                                massOut = self.mass*self.spacetime.massTransfer
                                                self.mass -= massOut
                                                particle.mass += massOut
                                                distanceToMove = (self.radiusf + particle.radiusf) - self.distance(particle)
                                                angle = 0
                                                if self.x-particle.x == 0:
                                                        if (self.x-particle.x)>0:
                                                                angle = np.pi/2
                                                        if (self.x-particle.x)<0:
                                                                angle = 3*np.pi/2
                                                else:
                                                        angle = np.arctan((particle.y-self.y)/(particle.x-self.x))
                                                
                                                self.x += np.cos(angle)*distanceToMove
                                                self.y += np.sin(angle)*distanceToMove

                                                total_xmomentum = particle.px + self.px
                                                total_ymomentum = particle.py + self.py

                                                self.dx = (total_xmomentum/self.mass)*self.spacetime.bounceRegulator*self.spacetime.tickrate
                                                self.dy = (total_ymomentum/self.mass)*self.spacetime.bounceRegulator*self.spacetime.tickrate

        def behave(self,tickrate):
                self.gravity()
                self.velocity()
                self.recolor()
                pg.draw.circle(self.spacetime.win, self.color, self.pos, self.radius)

        def force(self,leadpoint,force):
                x,y = leadpoint[0], leadpoint[1]
                self.dx += (((x-self.x)*force)/self.mass)
                self.dy -= (((y-self.y)*force)/self.mass)