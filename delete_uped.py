#-*- coding:utf-8 -*-

import os
import shutil

def delete_uped():
	file_name = os.listdir(os.getcwd())
	for fn in file_name:
		if os.path.isdir(fn):
			shutil.rmtree(fn)