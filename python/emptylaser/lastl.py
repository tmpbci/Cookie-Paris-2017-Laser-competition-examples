"""

3D Cube laser animation

by Sam Neurohack 
from /team/laser

 Display stl files : no optimisation will fail with very little points
 stl_mesh.vectors[faces][vertices (3)][coordonnees (3)]

"""

from globalVars import *
import frame
import sys, math, random
from stl import mesh
import numpy as np


SPEED = 4
SIZE = 40

class LASTL(object):
	
	def __init__(self):

		self.width = screen_size[0]
		self.height = screen_size[1]

		self.stlmesh = mesh.Mesh.from_file('files/ship1.stl')
		self.faces = len(self.stlmesh.vectors)
		self.stlmesh.rotate((0.5, 0.19, 0.0), math.radians(90))

		self.fov = 256
		self.viewer_distance = 450
		
		
		self.centerX = self.width / 2
		self.centerY = self.height / 2
		


	def Project(self):		

		
		self.laspoints = []
		
		for faces in range(len(self.stlmesh.vectors)):

			#print faces
			for lines in range(3):

				x = self.stlmesh.vectors[faces][lines][0]
				y = self.stlmesh.vectors[faces][lines][1]
				z = self.stlmesh.vectors[faces][lines][2]

				""" Transforms this 3D point to 2D using a perspective projection. """
				factor = self.fov / (self.viewer_distance + z)
				x = x * factor + self.centerX
				y = - y * factor + self.centerY
				self.laspoints.append((x,y))
				
		#print "Projected"



	def Rotate(self,angleX, angleY, angleZ):

		self.stlmesh.rotate([angleX, angleY, angleZ], math.radians(0.5))


	def Mode(self,centerX,centerY):

		self.centerX = centerX
		self.centerY = centerY	


	def Zoom(self, zoom):
	
		self.viewer_distance = zoom

	def Draw(self,f):

		f.PolyLineOneColor(self.laspoints, 0x00FF00,True)







