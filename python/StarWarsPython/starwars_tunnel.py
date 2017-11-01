#!/usr/bin/env python

"""
This file draws a 3d tunnel

the x,y and z coordinates of the tunnel are the coordinates of the observer in the tunnel
"""

import math
import random
import itertools
import sys
import time
import thread
import pygame

import dac
from common import *
from stream import PointStream
from shape import Shape
from color import *
from dimensions import *
import numpy

"""
CONFIGURATION
"""

try:
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    def get_joy():
        e = pygame.event.get()
        return 100.0*joystick.get_axis(0),100.0*joystick.get_axis(1),joystick.get_axis(5), joystick.get_axis(2)
except:
    def get_joy():
        return 0.0,0.0,-1.0,-1.0

LASER_POWER_DENOM = 1.0

ORIGIN_X = 0
ORIGIN_Y = 0

COLOR_R = CMAX / 1
COLOR_G = 0
#COLOR_G = CMAX / 1
COLOR_B = CMAX / 1

WAVE_SAMPLE_PTS = 500
WAVE_PERIODS = 0.5
WAVE_RATE = 0.2
WAVE_WIDTH = 42000 # XXX Not wavelength!
WAVE_AMPLITUDE_MAGNITUDE = 100 # dither between +/-
WAVE_AMPLITUDE_RATE = 50

"""
CODE BEGINS HERE
"""

def make_obstacle(left_side,vertical_center=0.0,height=0.2,width=0.2):
	if left_side:
		return [				  
		  [1.0, 1.0],
		  [1.0, vertical_center+0.5*height],
		  [1.0-width, vertical_center+0.5*height],
		  [1.0-width, vertical_center-0.5*height],
		  [1.0, vertical_center-0.5*height],
		  [1.0, -1.0],
		  [-1.0, -1.0],
		  [-1.0, 1.0]]
	else:
		return [				  
		  [1.0 ,  1.0   ],
		  [1.0 ,  -1.0  ],
		  [-1.0 ,  -1.0 ],
		  [-1.0 ,  vertical_center-0.5*height],
		  [-1.0+width,  vertical_center-0.5*height],
		  [-1.0+width, vertical_center+0.5*height],
		  [-1.0, vertical_center+0.5*height],
		  [-1.0, 1.0]]

class Tunnel(Shape):

	def __init__(self, x = 0, y = 0, r = 0, g = 0, b = 0,
			width = 10000, height = 2200):

		super(Tunnel, self).__init__(x, y, r, g, b)

		self.drawn = False
		self.origin = (0,0)
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		self.dz = 0.01 # speed in the z direction (towards the tunnel)
		self.dx = 0.5
		self.dy = 0.0
		self.ddx = 0.0
		self.ddy = 0.0
		self.points = []
		self.t = 0.0
                self.flag = False
		self.obstacles = []
		for i in [3.0,5.0,10.0,20.0,30.0,40.0,50.0]:
			self.obstacles.append((i,make_obstacle(random.randint(0,2)==0,
												   vertical_center=random.uniform(-0.5,0.5),
												   height=random.uniform(0.2,1.0),
												   width=random.uniform(2.0,2.0))))
	def produce(self):
		"""
		Generate the points of the circle.
		"""
		draw_diagonals = False
		r, g, b = (CMAX, CMAX*0.0, CMAX*0.0)
		r, g, b = (CMAX, CMAX, CMAX)
		self.t += 0.1
		self.z += self.dz
		self.x += 10.0*math.sin(0.05*self.t) # adding a bit of movement to the camera
		self.y += 10.0*math.sin(0.5*self.t)
                jx,jy, jf, jb = get_joy()
                self.x += jx
                self.y += jy
                self.dz = 0.03
                if jf > -1.0:
                    self.dz = 0.07
                if jf > 0.0:
                    self.dz = 0.3
                if jb < -0.9:
                    self.flag = False
                if jb > 0.9 and not self.flag:
                    self.flag = True
                    if len(self.obstacles) > 0:
    		        self.obstacles.pop()
                        self.obstacles.append((self.z + random.randint(20,50),
		             make_obstacle(random.randint(0,2)==0,
                             vertical_center=random.uniform(-0.5,0.5),
												   height=random.uniform(0.2,1.0),
												   width=random.uniform(2.0,2.0))))
			
		last_points = None
		for segment in range(6):
		        r, g, b = (0.0*CMAX, CMAX, 0.0*CMAX)
			distance = (segment+2) - (self.z)%1.0
			scale = 20000.0/distance # Scale factor for the tunnel
                        
			# we get the offset to the center point and scale it according to distance
			offset_x = 1.0*(self.x - self.origin[0]) * math.sqrt(math.sqrt(distance)) # the offset diminishes nonlinear with distance
			offset_y = 1.0*(self.y - self.origin[1]) * math.sqrt(math.sqrt(distance)) # somehow the fourth root looked ok
			# 2d model of one tunnel segment: |_|
			rect_points = [				  
					  [1.0, 1.0],
					  [1.0, -1.0],
					  [-1.0,  -1.0],
					  [-1.0, 1.0]]
			for (o,model) in self.obstacles:
				if math.floor(self.z + segment) <= o and math.ceil(self.z + segment) > o:
					# an obstacle replaces the whole section with a new model
		                        r, g, b = (CMAX, CMAX*0.0, CMAX*0.0)
					rect_points = model
				if self.z > o+2:
					# we are past this obstacle, so we can make a random new one
					self.obstacles.remove((o,model))
					self.obstacles.append((self.z + random.randint(20,50),
						                   make_obstacle(random.randint(0,2)==0,
												   vertical_center=random.uniform(-0.5,0.5),
												   height=random.uniform(0.2,1.0),
												   width=random.uniform(2.0,2.0))))
			rect_points = numpy.array(rect_points)
			rect_points *= scale
			rect_points[:,0] += offset_x
			rect_points[:,1] += offset_y
			if segment%2 == 0:
				# we invert every second rectangle
				# So that we can draw them continously
				rect_points = rect_points[::-1]
			if draw_diagonals and last_points is not None:
				for i in range(10):
					p = (last_points[-1][0] + i/10.0*(rect_points[0][0]-last_points[-1][0]),
						 last_points[-1][1] + i/10.0*(rect_points[0][1]-last_points[-1][1]))
					for duplicate_points in range(3):
						yield (self.x + p[0],self.y + p[1], r, g, b)
			for i in range(10):
				# corner
				yield (self.x + rect_points[0][0],self.y + rect_points[0][1], r, g, b)
			for p0,p1 in zip(rect_points[:-1],rect_points[1:]):
				for i in range(10):
					p = (p0[0] + i/10.0*(p1[0]-p0[0]),
						 p0[1] + i/10.0*(p1[1]-p0[1]))
					for duplicate_points in range(4):
						yield (self.x + p[0],self.y + p[1], r, g, b)
			for i in range(10):
				# corner
				yield (self.x + rect_points[-1][0],self.y + rect_points[-1][1], r, g, b)
			if draw_diagonals and last_points is not None:
				# diagonal to last rectange
				for i in range(10):
					p = (rect_points[-1][0] + i/10.0*(last_points[0][0]-rect_points[-1][0]),
						 rect_points[-1][1] + i/10.0*(last_points[0][1]-rect_points[-1][1]))
					for duplicate_points in range(3):
						yield (self.x + p[0],self.y + p[1], r, g, b)
			for i in range(10):
				# backtracking / blanking
				yield (self.x + rect_points[-1][0],self.y + rect_points[-1][1], 0,0,0)

			last_points = [[self.x + rect_points[0][0],self.y + rect_points[0][1]],
			               [self.x + rect_points[-1][0],self.y + rect_points[-1][1]]]
		self.drawn = True

def dac_thread():
	global l

	ps = PointStream()
	#ps.showTracking = True
	#ps.showBlanking = True
	ps.trackingSamplePts = 5
	ps.blankingSamplePts = 50

	l = Tunnel(0, 0, COLOR_R/LASER_POWER_DENOM,
							COLOR_G/LASER_POWER_DENOM,
							COLOR_B/LASER_POWER_DENOM)

	l.x = ORIGIN_X
	l.y = ORIGIN_Y

	#SQUARE.x = SQUARE_X
	#SQUARE.y = SQUARE_Y

	ps.objects.append(l)

	while True:
		try:
			d = dac.DAC(dac.find_first_dac())
			d.play_stream(ps)

		except KeyboardInterrupt:
			sys.exit()

		except Exception as e:
			import sys, traceback
			print '\n---------------------'
			print 'Exception: %s' % e
			print '- - - - - - - - - - -'
			traceback.print_tb(sys.exc_info()[2])
			print "\n"

def animate_thread():
	pass

def color_thread():

	while True:

		time.sleep(0.1)



#
# Start Threads
#

l = Tunnel()

thread.start_new_thread(dac_thread, ())
time.sleep(1.0)
thread.start_new_thread(animate_thread, ())
thread.start_new_thread(color_thread, ())

while True:
	inp = raw_input('Faster?')
	if inp.startswith('y'):
		l.dz *= 2.0
		print 'speed:',l.dz
	else:
		l.dz *= 0.5
		print 'speed:',l.dz
	time.sleep(0.1)

