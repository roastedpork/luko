#!/usr/bin/env python3
import sys
import time
import math
import random
import numpy as np
import pygame
import cv2

class ImageHandler(object):
	def __init__(self, file, grayscale = False):
		# load image
		img = cv2.imread(file, 0) if grayscale else cv2.imread(file,1)
                info = pygame.display.Info()

		# resize longer edge of the image to the shorter edge of the screen
		size = img.shape
		rows, cols = size[0],size[1]
		short_side = min(info.current_w,info.current_h)
		diag = math.sqrt(rows*rows + cols*cols)

		if len(size) == 3:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		new_size = (int(cols*short_side/max(size)), int(rows*short_side/max(size)))

		# member variables
		self.original = cv2.resize(img, dsize=new_size)
		self.diag = math.sqrt(new_size[0]*new_size[0] + new_size[1]*new_size[1])
	
		self.buffer = np.copy(self.original)
		self.rotated = False
		self.transformed = False
		self.grayscale = grayscale

	def rotate(self, rot):
		# performs rotation on the image before transformation
		if rot != 0:
			diag = int(self.diag)
			mid = diag/2
			temp = np.zeros((diag,diag), dtype = np.uint8) if self.grayscale else np.zeros((diag,diag,3), dtype = np.uint8)

			size = self.original.shape
			rows, cols = size[0], size[1]
			halfR,halfC = rows/2,cols/2
			if self.grayscale: temp[mid-halfR:mid+halfR,mid-halfC:mid+halfC] = self.original[0:2*halfR,0:2*halfC]
			else: temp[mid-halfR:mid+halfR,mid-halfC:mid+halfC,:] = self.original[0:2*halfR,0:2*halfC,:]
	

			# Generate map matrix
			M = cv2.getRotationMatrix2D((mid,mid), rot, 1.0)
			
			# Write to buffer
			self.buffer = cv2.warpAffine(temp, M, (diag,diag), flags = cv2.INTER_LINEAR)
			self.rotated = True

	def transform(self,theta):
		if theta != 0:
			# performs perspective transform on an OpenCV image depending on angle
			size = self.buffer.shape if self.rotated else self.original.shape
			rows, cols = size[0], size[1]
		
			# empirically obtained scaling factors
			scaleC = 2.5 #0.5
			scaleR = 2.5 #0.7	

			delC = int(scaleC*cols*(math.sin(math.radians(theta)))/2)
			delR = int(rows*scaleR*math.sin(math.radians(theta)))

			# Generate map matrix
			pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])			# src
			#pts2 = np.float32([[delC,0],[cols-delC,0],[cols,rows-delR],[0,rows-delR]])	# dst
			pts2 = np.float32([[0,0],[cols,0],[cols-delC,rows-delR],[delC,rows-delR]])	# dst
			M = cv2.getPerspectiveTransform(pts1,pts2)

			# Write to buffer
			self.buffer = cv2.warpPerspective(self.buffer if self.rotated else self.original,M,(cols,rows-delR))
		elif not self.rotated:
			self.buffer = np.copy(self.original)
	def display(self, screen, blitPoint = None):
		# display image on screen
		self.buffer = np.rot90(self.buffer)
		frame = pygame.surfarray.make_surface(self.buffer)
                info = pygame.display.Info()		
		# Calculate blitPoint to display at centre if not given
		if blitPoint == None: 
			size = self.buffer.shape
			cols, rows = size[0],size[1]
			blitPoint = ((info.current_w-cols)/2, (info.current_h-rows)/2)

		screen.blit(frame, blitPoint)
		self.rotated = False

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
