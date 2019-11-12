import sys
import os
import glob
import numpy as np
import skimage.io

files = glob.glob('*.jpg')


from PIL import Image



for num in range(int(len(files)/16)):
	sub_img = [ img for img in files if img.split('.')[0][2:] == str(num+1)]
	sub_img.sort()
	print (sub_img)
	
	temp = skimage.io.imread(sub_img[0]).shape

	all_width = temp[0]*4
	all_height = temp[1]*4

	result = Image.new("RGB", (all_width, all_height))

	x , y = 0, 0
	for i in [0, 1, 2, 3]:
		for j in [0, 1, 2, 3]:
		  img = Image.open(str(i)+str(j)+str(num)+'.jpg')
		  size = temp
		  result.paste(img, (x, y))
		  x += size[0]
		  
		y += size[1]
		x=0

	result.save(os.path.expanduser('image3/'+str(num)+'.jpg'))