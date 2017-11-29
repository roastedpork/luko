#!/usr/bin/env python3
import sys
import time
import math
import numpy as np
import pygame
import cv2

# dimension of the display
screen_cols = 1182 #1280
screen_rows = 624 #720

# initialise GUI environment
pygame.init()
flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.NOFRAME | pygame.FULLSCREEN
screen = pygame.display.set_mode((screen_cols,screen_rows), flags)
screen.fill([0,0,0])
pygame.mouse.set_visible(False)
pygame.display.set_caption("Luko")
clock = pygame.time.Clock()
info = pygame.display.Info()
print(info)




class ImageHandler(object):
	def __init__(self, file, grayscale = False):

		self.original = cv2.imread(file, 0) if grayscale else cv2.imread(file,1)
		self.buffer = np.copy(self.original)

	def transform(self,theta):
		# performs perspective transform on an OpenCV image depending on angle
		size = self.original.shape
		cols, rows = size[0], size[1]
		
		# empirically obtained scaling factors
		scaleC = 0.25
		scaleR = 0.5	

		delC = int(scaleC*cols*(math.sin(math.radians(theta)))/2)
		delR = int(rows*scaleR*math.sin(math.radians(theta)))

		# Generate map matrix
		pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])			# src
		pts2 = np.float32([[delC,0],[cols-delC,0],[cols,rows-delR],[0,rows-delR]])	# dst
		M = cv2.getPerspectiveTransform(pts1,pts2)

		# Write to buffer
		self.buffer = cv2.warpPerspective(self.original,M,(cols,rows-delR))

	def display(self, screen, blitPoint = None):
		# converts an OpenCV image buffer into a resized pygame image
		self.buffer = np.rot90(self.buffer)
		size = self.buffer.shape
		cols, rows = size[0],size[1]

		short_side = min(info.current_w,info.current_h)
		if len(size) == 3:
			self.buffer = cv2.cvtColor(self.buffer, cv2.COLOR_BGR2RGB)
		new_size = (int(size[1]*short_side/max(size)), int(size[0]*short_side/max(size)))

		self.buffer = cv2.resize(self.buffer, dsize=new_size)
		
		# display image on screen
		frame = pygame.surfarray.make_surface(self.buffer)
		if blitPoint == None: blitPoint = ((info.current_w-cols)/2, (info.current_h-rows)/2)
		screen.blit(frame, blitPoint)
		print(info.current_w,info.current_h)
		print(self.buffer.shape)
		print(blitPoint)


if __name__ == "__main__":
	# load cv2 image
	img = ImageHandler('grid30.png')
	img.transform(30)
	img.display(screen)
	pygame.display.update()

	# main running loop
	try:
		angle = 0
		while True:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					sys.exit(0)
				print(event)

			img.transform(angle)
			screen.fill([0,0,0])
			img.display(screen)
			angle = angle + 5 if angle < 90 else 0
			pygame.display.update()
			clock.tick(1)

	except KeyboardInterrupt or SystemExit:
		pygame.quit()
		cv2.destroyAllWindows()
