import core

from pygame.locals import *

class MyGame(core.Game):
	
	def event(self, event):
		# Calls the parent's behavior (optional)
		super(MyGame, self).event(event)

		# Adds news behavior to this method
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				print("Exiting...")
				self.running = False

if __name__ == '__main__':
	game = MyGame()
	game.setup()
	game.loop()