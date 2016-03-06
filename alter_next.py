#-*- coding:utf-8 -*-

import os

def alter_next():
	fr = open('next.txt','r')
	num_str = fr.read()
	fr.close()
	next_num_str = str(int(num_str)+1)
	fw = open('next.txt','w')
	fw.write(next_num_str)
	fw.close()