#-*- coding:utf-8 -*-

import os
import shutil
import time
from ugirl_1 import ugirl
from beauty3_1 import beauty3
from beauty5_1 import beauty5
from wechat_up import up_pub_try
from com_anti_800_1200 import com
from qn_up import up_pub

def delete_uped():
	file_name = os.listdir(os.getcwd())
	for fn in file_name:
		if os.path.isdir(fn):
			shutil.rmtree(fn)

def alter_pub(num):
	open('pub.txt','w').write(num)
	
def alter_next():
	fr = open('next.txt','r')
	num_str = fr.read()
	fr.close()
	next_num_str = str(int(num_str)+1)
	fw = open('next.txt','w')
	fw.write(next_num_str)
	fw.close()
	
def down_test():
	file_name = os.listdir(os.getcwd())
	for fn in file_name:
		if os.path.isdir(fn):
			return 1
	return 0
	
def pub_test():
	return int(open('pub.txt','r').read())

#下载成功后压缩
com()
#压缩过后就可以调用qn_up上传
up_pub()
alter_next()
#alter_pub('1')
delete_uped()