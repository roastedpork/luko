from PIL import Image
import numpy as np

img = Image.open("test.bmp")
rgb_im = img.convert('RGB')
print(rgb_im.size)

arr = np.array(rgb_im)

#print(arr[0])

nw_arr = arr[1:]
print(nw_arr)
new_arr = np.delete(nw_arr, [0,2])
print(new_arr)
new_img = Image.fromarray(new_arr, 'RGB')

new_img.save('test2.bmp')
