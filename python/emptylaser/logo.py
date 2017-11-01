# coding=UTF-8
'''
Created on 10 févr. 2015

@author: pclf
'''

import vectors
import gstt

LOGO = [
	# Etoile
	[[(-155,-95),(-135,-85)],0xFF00],
	[[(-155,-85),(-135,-95)],0xFF00],
	[[(-150,-100),(-140,-80)],0xFF00],
	# L/o
	[[(-140,-100),(-200,20),(120,20)],0xFF00],
	# aser
	[[(-140,-40),(-100,-40,),(-120,0),(-160,0),(-110,-20)],0xFFFF],
	[[(-40,-40),(-60,-40),(-90,-20),(-50,-20),(-80,0),(-100,0)],0xFFFF],
	[[(-30,-20),(10,-20),(0,-40),(-20,-40),(-30,-20),(-30,0),(-10,0)],0xFFFF],
	[[(20,0),(40,-40),(35,-30),(50,-40),(70,-40)],0xFFFF],
	]

#LOGO_OFFSET = vectors.Vector2D(200,-100)
LOGO_OFFSET = vectors.Vector2D(400,320)

def Draw(f):
	'''
	Dessine le logo
	'''
	for pl_color in LOGO:
		c = pl_color[1]
		xy_list = []
		for xy in pl_color[0]:
			xy_list.append((LOGO_OFFSET + vectors.Vector2D(xy[0],xy[1])).ToTuple())
		f.PolyLineOneColor(xy_list, c)




