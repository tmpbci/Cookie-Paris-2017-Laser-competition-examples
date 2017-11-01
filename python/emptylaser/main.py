# coding=UTF-8
'''
Empty Laser 
By Sam Neurohack
LICENCE : CC

You get a basic pygame skeleton to handle the laser drawing with an onscreen simulator.
This Empty Laser is mainly a Laser Hexagon (see /tmp/lab github) structure with some extras, like alignement keys.

Many things are still in the todo list as how to store the align parameters in globalVars for the next run.

'''


import pygame
import math
import random
import itertools
import sys
import os
import thread
import time
import frame
from vectors import Vector2D
import renderer
import dac
from globalVars import *
#import pylibmc
#mc = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})



# Import all objects generators


import gstt
import playertest
import cube
#import lastl
import score
import logo
import ship
import track



def StartPlaying(first_time = False):
	gstt.score.Reset()
	gstt.fs = GAME_FS_PLAY

	
def dac_thread():

	while True:
		try:

			d = dac.DAC(dac.find_first_dac())
			d.play_stream(laser)

		except Exception as e:

			import sys, traceback
			print '\n---------------------'
			print 'Exception: %s' % e
			print '- - - - - - - - - - -'
			traceback.print_tb(sys.exc_info()[2])
			print "\n"
			pass

def DrawTestPattern(f):
	l,h = screen_size
	L_SLOPE = 30
	
	f.Line((0, 0), (l, 0), 0xFFFFFF)
	f.LineTo((l, h), 0xFFFFFF)
	f.LineTo((0, h), 0xFFFFFF)
	f.LineTo((0, 0), 0xFFFFFF)
	
	f.LineTo((2*L_SLOPE, h), 0)
	for i in xrange(1,7):
		c = (0xFF0000 if i & 1 else 0) | (0xFF00 if i & 2 else 0) | (0xFF if i & 4 else 0)
		f.LineTo(((2 * i + 1) * L_SLOPE, 0), c)
		f.LineTo(((2 * i + 2) * L_SLOPE, h), c)
	f.Line((l*.5, h*.5), (l*.75, -h*.5), 0xFF00FF)
	f.LineTo((l*1.5, h*.5), 0xFF00FF)
	f.LineTo((l*.75, h*1.5), 0xFF00FF)
	f.LineTo((l*.5, h*.5), 0xFF00FF)
		
def Align(f):
	l,h = screen_size
	L_SLOPE = 30
	
	f.Line((0, 0), (l, 0), 0xFFFFFF)
	f.LineTo((l, h), 0xFFFFFF)
	f.LineTo((0, h), 0xFFFFFF)
	f.LineTo((0, 0), 0xFFFFFF)
	laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)

	print str(gstt.centerx) + "," + str(gstt.centery) + "," + str(gstt.zoomx) + "," + str(gstt.zoomy) + "," + str(gstt.sizex) + "," + str(gstt.sizey)
	

app_path = os.path.dirname(os.path.realpath(__file__))


# Pygame init


pygame.init()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Empty Laser")
clock = pygame.time.Clock()


# Main Variables init.

gstt.centerx = LASER_CENTER_X
gstt.centery = LASER_CENTER_Y
gstt.zoomx = LASER_ZOOM_X
gstt.zoomy = LASER_ZOOM_Y
gstt.sizex = LASER_SIZE_X
gstt.sizey = LASER_SIZE_Y
gstt.finangle = LASER_ANGLE


'''
Wipeout ship orientation 

vers la gauche :

gstt.cubeangleX = 4022
gstt.cubeangleY = 3780
gstt.cubeangleZ = 3741

vers devant :

gstt.cubeangleX = 4022
gstt.cubeangleY = 3782
gstt.cubeangleZ = 3059

vers la droite :

gstt.cubeangleX = 4022
gstt.cubeangleY = 3792
gstt.cubeangleZ = 3440

'''

gstt.cubeangleX = 4022
gstt.cubeangleY = 3776
gstt.cubeangleZ = 3059

gstt.cubecenterX = screen_size[0] / 2
gstt.cubecenterY = screen_size[1] / 2

cubespeed = 0

stlX = 0
stlY = 0
stlZ = 0 

turn = -20

current_string = 0 


# Laser handler init

fwork_holder = frame.FrameHolder()
laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)

thread.start_new_thread(dac_thread, ())


update_screen = False


# All laser object generators init 


gstt.score = score.Score()
gstt.plyr = playertest.PlayerTest()
gstt.cb = cube.Cube()
#gstt.lastl = lastl.LASTL()
#gstt.lastl.Project()
gstt.ship = ship.Ship()
gstt.trck = track.Track()




# Set start configuration

gstt.shipX = 400
gstt.shipY = 570
gstt.ship.Change(273,180,0)
gstt.shipXspeed = 10
gstt.ship.Move(gstt.shipX,gstt.shipY)

gstt.trackspeed = 0.008
gstt.maxspeed = 0.04
gstt.trck.Speed(gstt.trackspeed)


gstt.cb.Change(0,0,0)
counter = 0
gstt.demostate = 110
gstt.fs = GAME_FS_MENU

keystates = pygame.key.get_pressed()


# Main loop

while gstt.fs != GAME_FS_QUIT:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gstt.fs = GAME_FS_QUIT
	
	keystates_prev = keystates[:]
	keystates = pygame.key.get_pressed()[:]

	

	# Game Menu

	if gstt.fs == GAME_FS_MENU:
		if keystates[pygame.K_ESCAPE] and not keystates_prev[pygame.K_ESCAPE]:
			gstt.fs = GAME_FS_QUIT
		elif keystates[pygame.K_SPACE] and not keystates_prev[pygame.K_SPACE]:
			StartPlaying(True)
	elif gstt.fs == GAME_FS_PLAY:
	
	
	# Escape vers menu
		if keystates[pygame.K_ESCAPE] and not keystates_prev[pygame.K_ESCAPE]:
			gstt.fs = GAME_FS_MENU


	# anim playertest
		up_key = keystates[pygame.K_UP]
		down_key = keystates[pygame.K_DOWN]
		left_key = keystates[pygame.K_LEFT]
		right_key = keystates[pygame.K_RIGHT]
		
		#gstt.plyr.Move(up_key,down_key,left_key,right_key)
		
		
		
		# state 110 : WIPEOUT
		
		if gstt.demostate == 110:
				
				#if cubespeed < 6 :
			
				
				#print turn
				gstt.trck.Turn(turn)
				turn += 0.03
				if turn > 20:
					turn = -20

				
				#print gstt.shipX , gstt.trackspeed
				
				if gstt.shipX < 100 or gstt.shipX >700 :
					if gstt.trackspeed >= 0.001:
						gstt.trackspeed -= 0.001
						gstt.trck.Speed(gstt.trackspeed)
					
				else:
					if gstt.trackspeed < gstt.maxspeed:
						gstt.trackspeed += 0.0001
						gstt.trck.Speed(gstt.trackspeed)


					
				gstt.ship.Change(4022,3780,3780)
				
				#print left_key,gstt.shipX
				if left_key and gstt.shipX > 10:
					gstt.shipX -= gstt.shipXspeed
					gstt.ship.Move(gstt.shipX,gstt.shipY)
					gstt.ship.Change(4022,3792,3440)
					
				if right_key and gstt.shipX < 790 :
					gstt.shipX += gstt.shipXspeed
					gstt.ship.Move(gstt.shipX,gstt.shipY)
					gstt.ship.Change(4022,3772,3059)
					
				if keystates[pygame.K_i]:
					gstt.cubeangleX += cubespeed
				if keystates[pygame.K_o]:
					gstt.cubeangleY += cubespeed
				if keystates[pygame.K_p]:
					gstt.cubeangleZ += cubespeed
				
		
		
		# state 100 : DISPLAY STL FILE
		
		if gstt.demostate == 100:
		
				counter += 0.001
				#stlX += 0.01
				stlY += 0.01
				#stlZ += 0.01
				gstt.lastl.Rotate(stlX,stlY,stlZ)
				gstt.lastl.Project()
				print counter
				
		
		
		# state 90-93 : CUBE ANIMATION
				
		if gstt.demostate == 90:					# start
				
				
				counter += 0.001
				
				if counter > 0.1 and counter < 0.11:
					gstt.cb.Change(0.4,0.4,0.4)
				if counter > 0.11 and counter < 0.2:
					gstt.cb.Change(0,0,0)
					
				if counter > 0.2 and counter < 0.21:
					gstt.cb.Change(0.8,0.8,0.8)
				if counter > 0.21 and counter < 0.22:
					gstt.cb.Change(0,0,0)	
					
				if counter > 0.3:
					counter = 0
					gstt.demostate = 91
					
					
		if gstt.demostate == 91:
				
				if cubespeed < 6 :
					print cubespeed
					cubespeed += 0.008
					gstt.cubeangleX += cubespeed
					gstt.cubeangleY += cubespeed
					#gstt.cubeangleZ += cubespeed
					#@gstt.cb.Change(gstt.cubeangleX,gstt.cubeangleY,gstt.cubeangleZ)
					
				else:
					
					sinamp = 4 
					sinfreq = 5
					sindeltaX = 1
					sindeltaY = 0
					sinspeed = - 0.7
					gstt.demostate = 92
		
		if gstt.demostate == 92:
				
				if cubespeed > 0.5 :
					print cubespeed
					cubespeed -= 0.008
					gstt.cubeangleX += cubespeed
					gstt.cubeangleY += cubespeed
					#gstt.cubeangleZ += cubespeed
					gstt.cb.Change(gstt.cubeangleX,gstt.cubeangleY,gstt.cubeangleZ)
					
					
					# How to move the cube
					# sinusoid : y = Asin(B(x - C)) + D 
					# where A is the amplitude, B is the frequency, C is the horizontal shift and D is the vertical shift
					gstt.cubecenterX += sinspeed
					gstt.cubecenterY += sindeltaY + sinamp * math.sin(sinfreq * (gstt.cubecenterX - sindeltaX) * math.pi / 180)
					if gstt.cubecenterX < 0:
						gstt.cubecenterX = screen_size[0]
					
					gstt.cb.Move(gstt.cubecenterX,gstt.cubecenterY)
					
					
					
				if cubespeed <= 0.5 and cubespeed > 0.001 :
					cubespeed -= 0.001
					print cubespeed
					gstt.cubeangleX += cubespeed
					gstt.cubeangleY += cubespeed
					#gstt.cubeangleZ += cubespeed
					gstt.cb.Change(gstt.cubeangleX,gstt.cubeangleY,gstt.cubeangleZ)
					
					gstt.cubecenterX += sinspeed
					gstt.cubecenterY += sindeltaY + sinamp * math.sin(sinfreq * (gstt.cubecenterX - sindeltaX) * math.pi / 180)
					if gstt.cubecenterX < 0:
						gstt.cubecenterX = screen_size[0]
					
					gstt.cb.Move(gstt.cubecenterX,gstt.cubecenterY)
					
					
				if cubespeed < 0:
					print cubespeed
					gstt.cb.Change(0,0,0)
					gstt.demostate = 93
					zoom  = 3.2

		if gstt.demostate == 93:
		
				zoom -= 0.005
				gstt.cb.Zoom(zoom)
				if zoom < 0.005:
					gstt.fs == GAME_FS_GAMEOVER



		# state 10 : 
		
		if gstt.demostate == 10:
	
	
				gstt.cubeangleX += 1
				gstt.cubeangleY += 1
				gstt.cubeangleZ += 1
		
				gstt.cb.Change(gstt.cubeangleX,gstt.cubeangleY,gstt.cubeangleZ)
		
				gstt.cb.Move(gstt.cubecenterX,gstt.cubecenterY)
		
		
		

	elif gstt.fs == GAME_FS_GAMEOVER:

		if keystates[pygame.K_SPACE] and not keystates_prev[pygame.K_SPACE]:
			StartPlaying(False)

		elif keystates[pygame.K_ESCAPE] and not keystates_prev[pygame.K_ESCAPE]:
			gstt.fs = GAME_FS_MENU
		



	# DISPLAY management

	# On efface l'ecran avant + Création de la nouvelle frame vide où les objets du jeu vont dessiner
	
	screen.fill(0)
	fwork = frame.Frame()
	
	# Alignement Case
	
	if keystates[pygame.K_p]:
		DrawTestPattern(fwork)
		
	if keystates[pygame.K_x]:
		Align(fwork)
		
	if keystates[pygame.K_r]:
		gstt.centerx += 20
		Align(fwork)

	if keystates[pygame.K_t]:
		gstt.centerx -= 20
		Align(fwork)
		
	if keystates[pygame.K_y]:
		gstt.centery += 20
		Align(fwork)

	if keystates[pygame.K_u]:
		gstt.centery -= 20
		Align(fwork)

	if keystates[pygame.K_f]:
		gstt.zoomx += 0.1
		Align(fwork)

	if keystates[pygame.K_g]:
		gstt.zoomx -= 0.1
		Align(fwork)
		
	if keystates[pygame.K_h]:
		gstt.zoomy += 0.1
		Align(fwork)

	if keystates[pygame.K_j]:
		gstt.zoomy -= 0.1
		Align(fwork)
	
	if keystates[pygame.K_c]:
		gstt.sizex -= 50
		Align(fwork)
		
	if keystates[pygame.K_v]:
		gstt.sizex += 50
		Align(fwork)
		
	if keystates[pygame.K_b]:
		gstt.sizey -= 50
		Align(fwork)
		
	if keystates[pygame.K_n]:
		gstt.sizey += 50
		Align(fwork)
		
	if keystates[pygame.K_l]:
		gstt.finangle -= 0.001
		Align(fwork)
		
	if keystates[pygame.K_m]:
		gstt.finangle += 0.001
		Align(fwork)

	else:


		display_plyr = gstt.fs == GAME_FS_PLAY or gstt.fs == GAME_FS_GAMEOVER
		if display_plyr:
		
			#gstt.plyr.Draw(fwork)

			
			if 89 < gstt.demostate < 99:
				gstt.cb.Draw(fwork)
				
			if  gstt.demostate == 100:
				gstt.lastl.Draw(fwork)
			
			if gstt.demostate == 110:
				gstt.trck.Draw(fwork)
				gstt.ship.Draw(fwork)
				
			
		if gstt.fs == GAME_FS_MENU:
			logo.Draw(fwork)
			
	
	# Affecter la frame construite à l'objet conteneur de frame servant au système de rendu par laser
	
	
	fwork_holder.f = fwork

	if update_screen:
		update_screen = False
		fwork.RenderScreen(screen)
		pygame.display.flip()
	else:
		update_screen = True

	
	# TODO : rendre indépendante la fréquence de rafraîchissement de l'écran par
	# rapport à celle de l'animation du jeu
	clock.tick(100)

pygame.quit()


