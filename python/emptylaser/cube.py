"""

3D Cube laser animation

by Sam Neurohack 
from /team/laser

 Based on Wireframe 3D cube simulation.
 Developed by Leonel Machava <leonelmachava@gmail.com>

 
"""

from globalVars import *
import frame
import sys, math, random


SPEED = 4
SIZE = 40

class Cube(object):
	
	def __init__(self):

		self.width = screen_size[0]
		self.height = screen_size[1]


		self.vertices = [
            (- 1.0, 1.0,- 1.0),
            ( 1.0, 1.0,- 1.0),
            ( 1.0,- 1.0,- 1.0),
            (- 1.0,- 1.0,- 1.0),
            (- 1.0, 1.0, 1.0),
            ( 1.0, 1.0, 1.0),
            ( 1.0,- 1.0, 1.0),
            (- 1.0,- 1.0, 1.0)
			]

		# Define the vertices that compose each of the 6 faces. These numbers are
		# indices to the vertices list defined above.
		# self.faces = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
		self.faces = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
		
		self.fov = 256
		self.viewer_distance = 2.2
		
		
		self.centerX = self.width / 2
		self.centerY = self.height / 2


	def Change(self,angleX,angleY,angleZ):
	
			self.pointsX = []
			self.pointsY = []

			for v in self.vertices:
			
				# Rotate the point around X axis, then around Y axis, and finally around Z axis.
				
				x = v[0]
				y = v[1]
				z = v[2]
			
	
				
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
				self.pointsX.append(x)
				self.pointsY.append(y)	
				
				
		
	def Move(self,centerX,centerY):
	
		self.centerX = centerX
		self.centerY = centerY	

	def Mode(self,centerX,centerY):
	
		self.centerX = centerX
		self.centerY = centerY	
		
		
	def Zoom(self, zoom):
	
		self.viewer_distance = zoom

	def Draw(self,f):

		for fa in self.faces:

			#print fa
			#print self.pointsX[fa[0]],self.pointsY[fa[0]],self.pointsX[fa[1]],self.pointsY[fa[1]],self.pointsX[fa[2]],self.pointsY[fa[2]],self.pointsX[fa[3]],self.pointsY[fa[3]],self.pointsX[fa[0]],self.pointsY[fa[0]]
			#print self.pointsX[fa[0]],self.pointsY[fa[0]],self.pointsX[fa[1]],self.pointsY[fa[1]]
			
			f.PolyLineOneColor([(self.pointsX[fa[0]],self.pointsY[fa[0]]),(self.pointsX[fa[1]],self.pointsY[fa[1]]),(self.pointsX[fa[2]],self.pointsY[fa[2]]),(self.pointsX[fa[3]],self.pointsY[fa[3]]),(self.pointsX[fa[0]],self.pointsY[fa[0]])], 0xFFFFFF,True)







