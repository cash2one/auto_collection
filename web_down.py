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
from cut_uped import cut_uped 

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

def main():
	#umei.cc
	if pub_test() == 0:
		try:
			beauty3()
		except:
			f = open('error_log.txt','a')
			f.write('beauty3 error ' + time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time())) + '\n')
			f.close()
		#测试是否下载成功
		if down_test() == 1:
			#下载成功后压缩
			#com()
			#压缩过后就可以调用qn_up上传
			up_pub()
			if up_pub_try() == 1:
				alter_next()
				alter_pub('1')
				cut_uped('D:\\professor')
				return 'S'
	#beautylegmm.com
	if pub_test() == 0:
		try:
			beauty5()
		except:
			f = open('error_log.txt','a')
			f.write('beauty5 error ' + time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time())) + '\n')
			f.close()
		if down_test() == 1:
			#下载成功后压缩
			#com()
			#压缩过后就可以调用qn_up上传
			up_pub()
			if up_pub_try() == 1:
				alter_next()
				alter_pub('1')
				cut_uped('D:\\professor')
				return 'S'

if __name__=='__main__':
	main()
