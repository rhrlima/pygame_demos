import pygame as pg
from pygame.locals import *

class Game:

	WINDOW_WIDTH  = 400
	WINDOW_HEIGHT = 400
	FPS = 30

	def __init__(self):
		self.surface = None
		self.clock = None
		self.running = None

	def setup(self):
		pg.init()
		pg.display.set_caption("base demo")
		self.surface = pg.display.set_mode( (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pg.HWSURFACE )
		self.clock = pg.time.Clock()
		self.running = True

	def teardown(self):
		pg.quit()
		quit()

	def event(self, event):
		if event.type == QUIT:
			self.running = False
		print(event)

	def update(self):
		pass
	
	def draw(self):
		pass
	
	def loop(self):
		while self.running:
			self.clock.tick(self.FPS)
			for event in pg.event.get():
				self.event(event)
			self.update()
			self.draw()
		self.teardown()