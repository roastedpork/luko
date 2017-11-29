import numpy as np
import cv2



img = 255 * np.ones((720,1280),dtype=np.uint8)

for i in range(0,720,40):
	img[i,:] = np.zeros((1,1280))
for j in range(0,1280,40):
	img[:,j] = np.zeros(720)


cv2.imwrite('grid_rect.png',img)
#cv2.imshow('',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
