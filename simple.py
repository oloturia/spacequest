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
boomer_steer = pygame.image.load("boomer01_steer.png")
bullet = pygame.image.load("bullet.png")
tachonoid01 = pygame.image.load("tachonoid01.png")
tachonoid02 = pygame.image.load("tachonoid02.png")
explosion = pygame.image.load("explo.png")


def rot_sprite(image,rect,angle):
	rot_image = pygame.transform.rotate(image,angle)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect

#targets definition
class Tachonoid(pygame.sprite.Sprite):
	def __init__(self,formation):
		self.y = 0
		self.formation = formation
		if self.formation == 1 or self.formation == 2:
			self.image = tachonoid01
			self.phase1 = numpy.random.randint(10,40)
			self.phase2 = numpy.random.randint(60,100)
			
			if formation == 1:
				self.x = 0
			else:
				self.x = WIDTH
		elif formation == 3 or formation == 4:
			self.phase1 = HEIGHT-10
			self.phase2 = 5
			self.phase3 = HEIGHT-10
			self.image = tachonoid02
			self.x = numpy.random.randint(10,WIDTH-9)
		pygame.sprite.Sprite.__init__(self)
		self.image = tachonoid01
		self.rect = self.image.get_rect()
		self.rect.y = self.y
		self.rect.x = self.x
		self.step = 0
		all_sprites.add(self)
		enemies.add(self)
	
	def hit(self):
		self.kill()

	def update(self):
		self.step += 1
		if self.formation == 1:
			if self.step < self.phase1:
				self.y += 6
			elif self.step == self.phase1:
				self.image,self.rect = rot_sprite(self.image,self.rect,45)
			elif self.step > self.phase1 and self.step < self.phase2:
				self.y += 3
				self.x += 3
			elif self.step == self.phase2:
				self.image,self.rect = rot_sprite(self.image,self.rect,45)
			elif self.step > self.phase2:
				self.x += 3
		if self.formation == 2:
			pass
		if self.formation == 3:
			pass
		if self.formation == 4:
			pass
		self.rect.x = self.x
		self.rect.y = self.y

#bullet definition
class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):

		pygame.sprite.Sprite.__init__(self)
		self.image = bullet
		self.rect = self.image.get_rect()

		self.x = x
		self.y = y
		self.speed = -10
		self.rect.y = self.y+self.speed
		self.rect.x = self.x
		all_sprites.add(self)
		bullets.add(self)

	def update(self):
		self.y += self.speed
		self.rect.y = self.y
		if self.y > HEIGHT:
			self.kill()


#player definition
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.rotate(boomer,180)

		self.x = WIDTH/2
		self.y = HEIGHT -30
		self.rect = self.image.get_rect()
		self.rect.y = self.y		

		self.alternate = True

		self.trigger_delay = 50
		self.last_trigger = 0
		self.recoil = 0.1

	def update(self):
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.image = pygame.transform.flip(pygame.transform.rotate(boomer_steer,180),True,False)
			self.x -=5
			if self.x < 0:
				self.x = 0
		if keystate[pygame.K_RIGHT]:
			self.image = pygame.transform.rotate(boomer_steer,180)
			self.x +=5
			if self.x > WIDTH-30:
				self.x = WIDTH-30
		if not(keystate[pygame.K_LEFT] or keystate[pygame.K_RIGHT]):
			self.image = pygame.transform.rotate(boomer,180)
		if keystate[pygame.K_UP]:
			pass
		if keystate[pygame.K_DOWN]:
			pass
		if keystate[pygame.K_SPACE]:
			if pygame.time.get_ticks() > self.last_trigger + self.trigger_delay:
				self.last_trigger = pygame.time.get_ticks()
				if self.alternate:
					self.offset = 5
				else:
					self.offset = 20
				new_bullet = Bullet(self.x+self.offset,self.y)	
				self.alternate = not self.alternate

		self.rect.x = self.x


all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
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
#new enemies
	if pygame.time.get_ticks() % 100 == 0:
		enemy = Tachonoid(1)

#hit enemy
	for hit_scan in bullets:
		for enemy_scan in enemies:
			if hit_scan.rect.colliderect(enemy_scan.rect):
				hit_scan.kill()
				enemy_scan.hit()

#update
	all_sprites.update()

#render
	screen.fill(BLACK)
	all_sprites.draw(screen)
	pygame.display.update()

pygame.quit()
