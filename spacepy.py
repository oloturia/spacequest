#!/usr/bin/python3
import random
import pygame
import numpy

#setup

#game const
WIDTH = 600
HEIGHT = 600
FPS = 60

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#pygame init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Blasterdhaus")
clock = pygame.time.Clock()

boomer = pygame.image.load("boomer01.png")
bullet = pygame.image.load("bullet.png")

bullet_clones = []

def xSinize(offset,rot,factor):
	return offset + numpy.sin(numpy.pi/180*rot) * factor

def yCosize(offset,rot,factor):
	return offset + numpy.cos(numpy.pi/180*rot) * factor

#bullet definition
class Bullet(pygame.sprite.Sprite):
	def __init__(self,startPos,rot):

		pygame.sprite.Sprite.__init__(self)
		self.image = bullet

		self.rect = self.image.get_rect()
		self.center = player.image.get_rect().center

		self.Xspeed = xSinize(0,rot,10)
		self.Yspeed = yCosize(0,rot,10)
		self.x = startPos[0]
		self.y = startPos[1]
		self.rot = rot

	def update(self):
		self.image = pygame.transform.rotate(bullet,self.rot)
		self.y += self.Yspeed
		self.x += self.Xspeed
		self.rect.y = self.y
		self.rect.x = self.x
		if self.y > HEIGHT or self.y < 0:
			self.kill()
		if self.x > WIDTH or self.x < 0:
			self.kill()


#player definition
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = boomer

		self.x = WIDTH/2
		self.y = HEIGHT/2
		self.rect = self.image.get_rect()
		self.center = self.image.get_rect().center

		self.Xspeed = 0
		self.Yspeed = 0
		self.rot = 0
		self.thrust = 0.1
		self.alternate = True

		self.a_offset = 0
		self.b_offset = 0
		
		self.trigger_delay = 50
		self.last_trigger = 0
		self.recoil = 0.1

	def update(self):
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.rot +=5
		if keystate[pygame.K_RIGHT]:
			self.rot -=5
		if keystate[pygame.K_UP]:
			self.Xspeed += xSinize(0,self.rot,self.thrust)
			self.Yspeed += yCosize(0,self.rot,self.thrust)
		if keystate[pygame.K_DOWN]:
			self.Xspeed -= xSinize(0,self.rot,self.thrust)
			self.Yspeed -= yCosize(0,self.rot,self.thrust)
		if keystate[pygame.K_SPACE]:
			if pygame.time.get_ticks() > self.last_trigger + self.trigger_delay:
				self.last_trigger = pygame.time.get_ticks()
				if self.alternate:
					self.offset = -10
				else:
					self.offset = 10
				
				tipX = self.x + xSinize(-3.5,self.rot,1)
				tipY = self.y + yCosize(-3.5,self.rot,1)
				tipX += xSinize(0,self.rot+90,self.offset)
				tipY += yCosize(0,self.rot+90,self.offset)
				bullet_clones.append(Bullet((tipX,tipY),self.rot))
				self.alternate = not self.alternate
				all_sprites.add(bullet_clones[len(bullet_clones)-1])
				self.Xspeed -= xSinize(0,self.rot,self.recoil)
				self.Yspeed -= yCosize(0,self.rot,self.recoil)

		self.image = pygame.transform.rotate(boomer,self.rot)
		self.x += self.Xspeed
		self.y += self.Yspeed
		self.rect.y = self.y
		self.rect.x = self.x
		self.rect = self.image.get_rect(center = (self.rect.x,self.rect.y))

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

#loop

running = True
while running:
	clock.tick(FPS)

#game events
	for event in pygame.event.get():
#quit
		if event.type == pygame.QUIT:
			running = False

#update
	all_sprites.update()

#render
	screen.fill(BLACK)
	all_sprites.draw(screen)
	pygame.display.update()

pygame.quit()
