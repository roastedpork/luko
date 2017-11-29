#!/usr/bin/env python3
import sys
import time
import numpy as np
import pygame
import cv2

# dimension of the display
screen_cols = 1280
screen_rows = 720


def processImage(img):
	# converts an OpenCV image into a pygame image
	img = np.rot90(img)
	size = img.shape
	short_side = min(screen_cols,screen_rows)
	if len(size) == 3:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	new_size = (int(size[1]*short_side/max(size)), int(size[0]*short_side/max(size)))

	return cv2.resize(img, dsize=new_size)


def transformImage(img, angle):
	# performs perspective transform on an image depending on angle
	size = img.shape
	print(size)
	rows, cols = size[0], size[1]

	# Generate map matrix
	pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])	# src
	pts2 = np.float32([[100,0],[cols-100,0],[cols,rows],[0,rows]])	# dst
	M = cv2.getPerspectiveTransform(pts1,pts2)

	return cv2.warpPerspective(img,M,(cols,rows))

def calcBlitPoint(img):
	# calculates the top left (?) position to centre the image onto the 720x720 display
	size = img.shape
	cols, rows = size[0],size[1]
	return ((screen_cols-cols)/2,(screen_rows-rows)/2)

if __name__ == "__main__":

	# initialise GUI environment
	pygame.init()
	flags = pygame.DOUBLEBUF | pygame.HWSURFACE #| pygame.NOFRAME | pygame.FULLSCREEN
	screen = pygame.display.set_mode((screen_cols,screen_rows), flags)
	screen.fill([0,0,0])
	pygame.display.set_caption("Luko")
	clock = pygame.time.Clock()

	# load cv2 image
	#img = cv2.imread('dog_bg_black.jpg',1)
	img = cv2.imread('grid_rect.png',1)
	img = transformImage(img,0)
	img = processImage(img)

	frame = pygame.surfarray.make_surface(img)
	
	screen.blit(frame, calcBlitPoint(img))
	#screen.blit(frame, (0,0))
	pygame.display.update()

	# main running loop
	try:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				print(event)

			pygame.display.update()
			clock.tick(60)

	except KeyboardInterrupt or SystemExit:
		pygame.quit()
		cv2.destroyAllWindows()
