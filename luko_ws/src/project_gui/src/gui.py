#!/usr/bin/env python3
import sys
import time
import math
import random
import numpy as np
import pygame
import cv2
from imagehandler import ImageHandler


# dimension of the display
screen_cols = 1920 #1182
screen_rows = 1080 #624



class ScreenHandler(object):
    def __init__(self):
        # initialise GUI environment
        pygame.init()
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.NOFRAME | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((screen_cols,screen_rows), flags)
        self.screen.fill([0,0,0])
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Luko")
        self.clock = pygame.time.Clock()
        self.info = pygame.display.Info()

    def run(self):
        img = ImageHandler("luko/projection_mapping/images/grid30.png")
        
if __name__ == "__main__":
	# load cv2 image
	phi = 30
	theta = 0
	
	paths = ['images/grid30.png','images/grid_rect.png', 'images/dog_bg_black.jpg']	
	imgs = [ImageHandler(path) for path in paths]
	ind = 0


	# main running loop
	try:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					sys.exit(0)
				print(event)

			imgs[ind].rotate(phi)
			imgs[ind].transform(theta)
			screen.fill([0,0,0])
			imgs[ind].display(screen)
			theta = theta + 3 if theta < 90 else 0
			pygame.display.update()
			if random.randint(0,20) < 2: ind = 0 if ind else 1
			clock.tick(60)

	except KeyboardInterrupt or SystemExit:
		pygame.quit()
		cv2.destroyAllWindows()
