"""

3D Cube laser animation

by Sam Neurohack 
from /team/laser

 Based on Wireframe 3D cube simulation.
 Developed by Leonel Machava <leonelmachava@gmail.com>

 Wipeout style ship 

"""

from globalVars import *
import frame
import sys, math, random



SPEED = 4
SIZE = 40

class Ship(object):
	
	def __init__(self):

		self.width = screen_size[0]
		self.height = screen_size[1]


		self.vertices = [
		( 0.1945572 , 0.3603683 , 0.7174169 ),
		( 0.1945572 , -4.39773 , 0.09228338 ),
		( 0.6054428 , 0.3603683 , 0.3174169 ),
		( 0.1945572 , 0.3603683 , 0.7174169 ),
		( -0.2854428 , 0.3603683 , 0.7174169 ),
		( -0.2854428 , -4.39773 , 0.09228338 ),
		( -0.614193 , 0.4115218 , 0.1858825 ),
		( -0.2854428 , 0.3603683 , 0.7174169 )
			]

		self.fov = 256
		self.viewer_distance = 3.2
		
		
		self.centerX = self.width / 2
		self.centerY = self.height / 2
		
		
		

	def Change(self,angleX,angleY,angleZ):
	
			self.laspoints = []

			for v in self.vertices:
			
			
				# Rotate the point around X axis, then around Y axis, and finally around Z axis.

				x = v[0]
				y = v[1]
				z = v[2]
				
				#print "(", (x+0.5), ",", y, "," ,z,"),"

				rad = angleX * math.pi / 180
				cosa = math.cos(rad)
				sina = math.sin(rad)
				y2 = y
				y = y2 * cosa - z * sina
				z = y2 * sina + z * cosa

				rad = angleY * math.pi / 180
				cosa = math.cos(rad)
				sina = math.sin(rad)
				z2 = z
				z = z2 * cosa - x * sina
				x = z2 * sina + x * cosa

				rad = angleZ * math.pi / 180
				cosa = math.cos(rad)
				sina = math.sin(rad)
				x2 = x
				x = x2 * cosa - y * sina
				y = x2 * sina + y * cosa


				""" Transforms this 3D point to 2D using a perspective projection. """
				factor = self.fov / (self.viewer_distance + z)
				x = x * factor + self.centerX
				y = - y * factor + self.centerY
				
				self.laspoints.append((x,y))

	def Move(self,centerX,centerY):
	
		self.centerX = centerX
		self.centerY = centerY	

	def Mode(self,centerX,centerY):
	
		self.centerX = centerX
		self.centerY = centerY	
		
		
	def Zoom(self, zoom):
	
		self.viewer_distance = zoom
				
				

	def Draw(self,f):

		f.PolyLineOneColor(self.laspoints, 0xFFFF00,True)
		
	








