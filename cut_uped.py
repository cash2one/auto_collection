# -*- coding:utf-8 -*-
import os
import shutil
import time
'''
def cutfile(src_path,dst_path):
	files = os.listdir(src_path)
	srcs=[]
	for file in files:
		srcs.append(os.path.join(src_path,file))
	for src in srcs:
		shutil.move(src,dst_path)
'''
		
def cut_uped(dst_path):
	file_name = os.listdir(os.getcwd())
	for fn in file_name:
		if os.path.isdir(fn):
			src = os.path.join(os.getcwd(),fn)
			shutil.move(src,dst_path)


#cut_uped('D:\\professor')








