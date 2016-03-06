# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import time
import sys
import os
import socket

#自己定义一个异常类
class urlerror(Exception):
	pass

def getHtml(url):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
	headers = { 'User-Agent' : user_agent }
	i = 0
	flag = 0
	while i < 1:
		try:
			request = urllib2.Request(url,headers = headers)
			response = urllib2.urlopen(request,timeout = 5)
			html = response.read()
			response.close()
			#page = urllib.urlopen(url)
			#html = page.read()
			#page.close()
			i += 1 
		except:
			if flag == 0:
				print u'打开网页失败，请检查网络'
			if flag == 5:
				print u'多次尝试打不开，结束程序'
				raise urlerror('Cant open URL')
			flag += 1
			time.sleep(1)
	return html
		
def getImg(html,name,x):
	reg = r'border=0 src=(.+?\.jpg) alt='
	imgre = re.compile(reg)
	imglist = re.findall(imgre,html)
	if imglist!=[]:
		#print imglist
		i = 0
		n = len(imglist)
		path = name + '\\' + '%s.jpg'
		flag = 0                                                     #用于提示语的控制
		while i < n:
			try:
				urllib.urlretrieve(imglist[i],path % x)
				i += 1
				time.sleep(1)
				x += 1
				flag = 0
			except:
				if flag == 0:
					print u'请等待...'
				if flag == 5:
					print u'下载出错，仍然尝试下载中，可继续等待或稍后再试'
				flag += 1
				time.sleep(5)
	return x
	
#重新写一种下载图片的方式，感觉urlretrieve这个函数有问题
def getImg2(html,name,x):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
	headers = { 'User-Agent' : user_agent }
	reg = r'<a href="(.+?)" target="_blank" title'	#这个要根据实际的图片地址,进行正则匹配,其实可以设置一个接口传入,有时候地址还需要拼接，所以写个统一的函数应该还需要分情况
	imgre = re.compile(reg)
	imglist_part = re.findall(imgre,html)
	imglist = []
	for e_imglist_part in imglist_part:
		imglist.append('http://www.beautylegmm.com' + e_imglist_part)
	if imglist!=[]:
		#print imglist
		i = 0
		n = len(imglist)
		
		flag = 0                                                     #用于提示语的控制
		while i < n:
			try:
				path = name + '\\' + str(x) + '.jpg'
				request = urllib2.Request(imglist[i],headers = headers)
				response = urllib2.urlopen(request,timeout = 5)
				print 'test0'
				data = response.read()
				response.close()
				print 'test1'				
				f = open(path,'wb')
				f.write(data)
				f.close()
				i += 1
				time.sleep(1)
				x += 1
				flag = 0
			except:
				print flag
				if flag == 0:
					print u'请等待...'
				if flag == 5:
					print u'下载出错，下载下一张'
					i += 1
					#可以写个日志记住那些下载出错的图片,也可以不要了
					fw = open('undown_list.txt','a')
					fw.write(path + '\n')
					fw.close()
					flag = 0
				flag += 1
				time.sleep(2)
	return x
	
#主函数	
def beauty5():
	page0 = 'http://www.beautylegmm.com/index-1.html'
	re1 = r'<a href="(.+?beauty.+?)" title="(.+?)" target="_blank"><img src='
	girl_html_re = re.compile(re1)
	page0_html = getHtml(page0)
	girl_html_list = re.findall(girl_html_re,page0_html)
	#print girl_html_list, 只要第一个girl, 不用for
	girl_html = girl_html_list[0]
	name = girl_html[1].strip().decode('utf-8').encode('GBK')
	#读取该下的期数
	if str(int(open('next.txt','r').read())+1) in name:
		x = 1
		print u'正在下载',name
		os.makedirs(name)
		html_every_girl = getHtml(girl_html[0])
		x = getImg2(html_every_girl,name,x)
		re2 = r'\d</a><a href="(.+?)" >'
		page_girl_html_re = re.compile(re2)
		page_list = re.findall(page_girl_html_re,html_every_girl)
		#for e_p_list in page_list:
			#print e_p_list 
		for page in page_list:
			final_html = getHtml(page)
			x = getImg2(final_html,name,x)
		return 1
	else:
		print name,u'已下载'
		return 0
			
if __name__ == '__main__':
	beauty5()

