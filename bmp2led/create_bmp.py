from PIL import Image

img = Image.new('RGB', (3,3), "white")
pixels = img.load()

img.save('test.bmp')
