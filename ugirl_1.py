# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import time
import sys
import os
import socket

def getHtml(url):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
	headers = { 'User-Agent' : user_agent }
	i = 0
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
			print u'打开网页失败，请检查网络'
			time.sleep(2)
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
				if flag == 20:
					print u'下载出错，仍然尝试下载中，可继续等待或稍后再试'
				flag += 1
				time.sleep(5)
	return x
	
#重新写一种下载图片的方式，感觉urlretrieve这个函数有问题
def getImg2(html,name,x):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
	headers = { 'User-Agent' : user_agent }
	reg = r'<a class="lightview thumb_wrap" rel="gallery-1" href="(.+?)" target="_blank">'	#这个要根据实际的图片地址,进行正则匹配,其实可以设置一个接口传入,有时候地址还需要拼接，所以写个统一的函数应该还需要分情况
	imgre = re.compile(reg)
	imglist = re.findall(imgre,html)
	print imglist
	if imglist!=[]:
		#print imglist
		i = 0
		n = len(imglist)
		
		flag = 0                                                     #用于提示语的控制
		while i < n:
			try:
				path = name + '\\' + str(x) + '.jpg'
				print path
				request = urllib2.Request(imglist[i],headers = headers)
				response = urllib2.urlopen(request,timeout = 5)
				print 'test0'
				data = response.read()
				response.close()
								
				f = open(path,'wb')
				print 'test1'
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



def ugirl():
	x = 1
	page0 = 'http://www.ugirl.cc/mztt'
	page0_html = getHtml(page0)
	#cd = time.strftime('%Y.%m.%d',time.localtime(time.time()))
	re1 = r'<h2><a href="(.+?)" target="_blank">(\[Beautyleg\].+?)<'
	date_re = re.compile(re1)
	girl_html = re.search(date_re,page0_html).group(1,2)
	name = girl_html[1].strip().decode('utf-8').encode('GBK')
	if str(int(open('next.txt','r').read())+1) in name:
		slt_page = getHtml(girl_html[0])
		os.makedirs(name)
		getImg2(slt_page,name,x)
	else:
		print name,u'已下载'
		
if __name__=='__main__':
	ugirl()

'''
re2 = r'<a class="lightview thumb_wrap" rel="gallery-1" href="(.+?)" target="_blank">'
image_re = re.compile(re2)
image_list = re.findall(image_re,slt_page)
print image_list
for img in image_list:
	getImg2(img,cd,x)
'''
