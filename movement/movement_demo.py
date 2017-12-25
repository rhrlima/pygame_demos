import core

import pygame as pg
from pygame.locals import *

WIN_W = 260 # window width
WIN_H = 260 # window height

# colors
BLACK = (  0,   0,   0)
BLUE  = (  0,   0, 200)
GREEN = (  0, 200,   0)
RED   = (200,   0,   0)
WHITE = (255, 255, 255)

#block size
SIZE = 20

#block speed
SPEED = 5

class Block:

	def __init__(self, x, y, color=WHITE):
		self.x = x
		self.y = y
		self.w = SIZE
		self.h = SIZE
		self.color = color
		self.direction = K_RIGHT
		self.speed = 0

	def update(self):
		if self.x > WIN_W + 5:
			self.x = - self.w
		elif self.x < -self.w - 5:
			self.x = WIN_W
		elif self.y > WIN_H + 5:
			self.y = - self.h
		elif self.y < -self.h - 5:
			self.y = WIN_H

	def draw(self, surface):
		pg.draw.rect(surface, self.color, self.get_rect())
		pg.draw.rect(surface, GREEN, self.get_rect(True), 1)

	def move(self):
		if self.direction == K_UP:
			self.y -= self.speed
		elif self.direction == K_DOWN:
			self.y += self.speed
		elif self.direction == K_LEFT:
			self.x -= self.speed
		elif self.direction == K_RIGHT:
			self.x += self.speed

		if SIZE == 16:
			#corrects the X and Y values to fit the grid
			if (self.x % SIZE == 15):   self.x += 1
			elif (self.x % SIZE ==  1): self.x -= 1
			if (self.y % SIZE == 15):   self.y += 1
			elif (self.y % SIZE ==  1): self.y -= 1

	def get_rect(self, next_step=False):
		rect = Rect(self.x, self.y, self.w, self.h)
		if next_step:
			if self.direction == K_UP:
				rect = Rect(self.x, self.y-self.speed, self.w, self.h)
			elif self.direction == K_DOWN:
				rect = Rect(self.x, self.y+self.speed, self.w, self.h)
			elif self.direction == K_LEFT:
				rect = Rect(self.x-self.speed, self.y, self.w, self.h)
			elif self.direction == K_RIGHT:
				rect = Rect(self.x+self.speed, self.y, self.w, self.h)
		return rect

	def intersects(self, other, next_step=False):
		#check if this block intersects other, flag to consider the block's direction
		return self.get_rect(next_step).colliderect(other.get_rect())


def can_move(block, objects):
	#checks if the block collides with any object from the list
	#flag = True
	for obj in objects:
		if block is not obj and block.intersects(obj, True):
			return False
	return True


class Game(core.Game):

	def setup(self):

		self.WINDOW_WIDTH = WIN_W
		self.WINDOW_HEIGHT = WIN_H

		super(Game, self).setup()
		
		#setting key repeat frequency (delay, interval)
		delay = 0
		interval = 15
		pg.key.set_repeat(delay, interval)
		
		self.movable = []
		self.objects = []

		#block
		self.block = Block(0, 0, BLUE)
		self.movable.append(self.block)
		
		for i in range(5): # X
			plat = Block(i * SIZE + i * SIZE + 2 * SIZE, i * 2 * SIZE + 2 * SIZE)
			plat.speed = SPEED
			self.movable.append(plat)

		for i in range(5): # Y
			plat = Block(i * 2 * SIZE + 2 * SIZE, i * SIZE + i * SIZE)
			plat.speed = SPEED
			plat.direction = K_UP
			self.movable.append(plat)

		for i in range(6):
			for j in range(6):
				self.objects.append(Block(i * 2 * SIZE + SIZE, j * 2 * SIZE + SIZE))

		self.objects += self.movable

	def event(self, event):
		#if hit X button
		if event.type == QUIT:
			self.running = False

		if event.type == KEYDOWN:
			#if pressed ESCAPE
			if event.key == K_ESCAPE:
				self.running = False

			#if pressed any of [up, down, left, right]
			available_keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
			#update the blocks's direction
			if event.key in available_keys:
				self.block.direction = event.key

				#if is not moving, set speed
				if self.block.speed == 0:
					self.block.speed = SPEED

	def update(self):
		# for each movable, checks if it can move
		for obj in self.movable:
			if can_move(obj, self.objects):
				obj.move()

		# for each object update it
		for obj in self.objects:
			obj.update()

	def draw(self):
		# fills the screen with black
		self.surface.fill(BLACK)

		#draws and updates objects
		for obj in self.objects:
			obj.draw(self.surface)

		#updates the draw buffer
		pg.display.flip()


if __name__ == '__main__':
	game = Game()
	game.setup()
	game.loop()