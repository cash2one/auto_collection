# -*- coding:utf-8 -*-

from PIL import Image
import os


#是否已经压缩过了
def is_com(path):
	fr = open('com.txt','r')
	#return 1 for record in fr if record.strip() == path
	for record in fr:
		if record.strip() == path:
			return 1
	return 0


#压缩文件夹下所有图片，并且用一个txt记录下压缩过的图片
#f = open('com.txt','a')
#f.close()
def com():
	file_name = os.listdir(os.getcwd())
	folder_name=[]
	for fn in file_name:
		if os.path.isdir(fn):
			folder_name.append(fn)
	for folder in folder_name:
		if is_com(folder) == 0:		
			#在每个文件夹下找到图片名的集合
			sub_dir = os.path.join(os.getcwd(),folder)
			img_name = os.listdir(sub_dir)
			#print img_name
			for img in img_name:
				print img	#test
				com_dir = os.path.join(sub_dir,img)
				#fr = open(com_dir,'rb')
				img = Image.open(com_dir)
				#fr.close()
				w,h = img.size
				if (w<=800 and h<=1200) or (w<=1200 and h<=800):
					pass
				else:
					print u'正在压缩:',com_dir
					if w < h:
						imgre = img.resize((800,1200),Image.ANTIALIAS)
						imgre.save(com_dir,'JPEG')
						#fw = open('com.txt','a')
						#fw.write(com_dir.split('\\')[-2] + '\n')
						#fw.close()
						#except Exception,e:
							#print str(e),com_dir
							#print u'文件损坏，正在删除:',com_dir
							#os.remove(com_dir)
					else:
						imgre = img.resize((1200,800),Image.ANTIALIAS)
						imgre.save(com_dir,'JPEG')
						#fw = open('com.txt','a')
						#fw.write(com_dir.split('\\')[-2] + '\n')
						#fw.close()
						#except Exception,e:
							#print str(e),com_dir
							#print u'文件损坏，正在删除:',com_dir
							#os.remove(com_dir)
			fw = open('com.txt','a')
			fw.write(folder + '\n')
			fw.close()

if __name__=='__main__':
	com()
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
