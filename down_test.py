#-*- coding:utf-8 -*-

import os

def down_test():
	file_name = os.listdir(os.getcwd())
	for fn in file_name:
		if os.path.isdir(fn):
			return 1
	return 0
