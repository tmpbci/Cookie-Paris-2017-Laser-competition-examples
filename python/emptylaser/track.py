#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

Wipeout Track Animation

by Sam Neurohack 
from /team/laser

 Based on Wireframe 3D cube simulation.
 Developed by Leonel Machava <leonelmachava@gmail.com>


"""

from globalVars import *
import frame
import sys, math, random



speed = 0.008
originY = 4.5
tracksize = 1.2


class Track(object):
	
	def __init__(self):


		self.fov = 256
		self.viewer_distance = 1.2
		
		self.width = screen_size[0]
		self.height = screen_size[1]
		self.centerX = self.width / 2
		self.centerY = self.height / 2

		self.lines = [originY,5,5.5,6]
		
		self.turn = -10
		self.turnabs = math.sin(self.turn * math.pi / 180) * self.centerX
		self.trackX = [self.centerX + (4*self.turnabs), self.centerX + (3*self.turnabs), self.centerX + (2*self.turnabs), self.centerX + self.turnabs, self.centerX]
		self.trackY = [math.exp(4.5), math.exp(5), math.exp(5.5), math.exp(6), math.exp(6.5)]
		self.speed = speed


	def Speed(self, speed):
	
		self.speed = speed
		
		

	def Turn(self, turn):
	
		self.turn = turn
		self.turnabs = math.sin(self.turn * math.pi / 180) * self.centerX
		self.trackX = [self.centerX + (4*self.turnabs), self.centerX + (3*self.turnabs), self.centerX + (2*self.turnabs), self.centerX + self.turnabs, self.centerX]
		self.trackY = [math.exp(4.5), math.exp(5), math.exp(5.5), math.exp(6), math.exp(6.5)]
				



	def Draw(self,f):
		
		print self.speed
		# increase lines Y position
		
		for l in range(len(self.lines)):

			self.lines[l] += self.speed
			#print l, self.lines[l]
			if self.lines[l] > 6.5:
				self.lines[l] = originY

		# sort result in m  

		m = self.lines
		m.sort()

		# start draw to the left

		directionX = -1


		# Go to road top

		f.LineTo(( self.trackX[0],math.exp(originY)),0x000000)
		
		for l in range(len(m)):
			
			trackh = math.exp(m[l])
			trackw = (math.exp(m[l]) - 80) / tracksize
			
			# line center x :  
			# % = (m[l] - 4.5)/2
			# x factor = 4 - (% * 4)
			# trackx = self.centerX + (x factor * self.turnabs)

			trackx = self.centerX + (self.turnabs * ( 4 - (m[l]-4.5)*2)) 
			#print trackx

			# draw to the left
			if directionX == -1:
				
				f.LineTo((trackx - trackw, trackh),0x000)		
				f.LineTo((trackx + trackw, trackh),0xFFFFFF)

			# draw to the right
			else: 
	
				f.LineTo((trackx + trackw, trackh),0x000)		
				f.LineTo((trackx - trackw, trackh),0xFFFFFF)
				
			# Change direction for next line

			directionX *= -1
			



		f.LineTo((self.trackX[4], math.exp(6.5)),0x000)



		# draw track borders bottom left - top - right bottom

		for l in range(4,-1,-1):
			f.LineTo( ((self.trackX[l] - ((self.trackY[l]) - 80) /tracksize), self.trackY[l]),0xFFFFFF)

		
		for l in range(5):
			f.LineTo( ((self.trackX[l] +  ((self.trackY[l]) - 80) /tracksize),self.trackY[l]),0xFFFFFF)
			

			
	







