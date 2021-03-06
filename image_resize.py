# -*- coding:utf-8 -*-

from PIL import Image
import os

'''
#是否已经压缩过了
def is_com(path):
	fr = open('com.txt','r')
	#return 1 for record in fr if record.strip() == path
	for record in fr:
		if record.strip() == path:
			return 1
	return 0
'''

#压缩文件夹下所有图片，并且用一个txt记录下压缩过的图片
#f = open('com.txt','a')
#f.close()
file_name = os.listdir(os.getcwd())
folder_name=[]
for fn in file_name:
	if os.path.isdir(fn):
		folder_name.append(fn)
for folder in folder_name:
	#在每个文件夹下找到图片名的集合
	sub_dir = os.path.join(os.getcwd(),folder)
	img_name = os.listdir(sub_dir)
	#print img_name
	for img in img_name:
		com_dir = os.path.join(sub_dir,img)
		img = Image.open(com_dir)
		w,h = img.size
		if (w==1600 and h==2400) or (w==2400 and h==1600):
			pass
		else:
			print u'正在压缩:',com_dir
			if w < h:
				imgre = img.resize((1600,2400))
			else:
				imgre = img.resize((2400,1600))
			imgre.save(com_dir,'JPEG')
'''
for fn in file_name:
	img = Image.open(fn)
	w,h = img.size
	if w < h:
		imgre = img.resize((1600,2400))
	else:
		imgre = img.resize((2400,1600))
	imgre.save(fn,'JPEG')
'''
