#-*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import requests
import poster
import re
import os
import time
from PIL import Image
import socket
import sys

#模拟登录
def log_in(username,pwd):
	paras = {'username':username,'pwd':pwd,'imgcode':'','f':'json'}
	req = urllib2.Request('https://mp.weixin.qq.com/cgi-bin/login',urllib.urlencode(paras))
	req.add_header('Accept','*/*')
	req.add_header('Accept-Encoding','gzip, deflate')
	req.add_header('Accept-Language','en-US,en;q=0.8')
	req.add_header('Connection','keep-alive')
	req.add_header('Content-Length','79')
	req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
	#req.add_header('Cookie','noticeLoginFlag=1; pgv_pvi=1648069632; noticeLoginFlag=1')
	req.add_header('Host','mp.weixin.qq.com')
	req.add_header('Origin','https://mp.weixin.qq.com')
	req.add_header('Referer','https://mp.weixin.qq.com/')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
	req.add_header('X-Requested-With','XMLHttpRequest')
	ret = urllib2.urlopen(req)
	retread = ret.read()
	retcontent = json.loads(retread)
	print retcontent['base_resp']['err_msg']
	#RedirectUrl = retcontent['redirect_url']	
	#token = RedirectUrl.split('token=')[1]	#另一种获取token的方式,split分割
	token = retcontent['redirect_url'][44:]
	print u'登录成功,token = ' + token
	return token

#私密消息
def s_msg(content):
	paras2 = {'token':token,'lang':'zh_CN','f':'json','ajax':1,'random':0.3910328117199242,'type':1,'content':content,'tofakeid':'2302469181','imgcode':''}
	#print paras2
	msgUrl = 'https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&f=json&token=' + token + '&lang=zh_CN'
	Referer = 'https://mp.weixin.qq.com/cgi-bin/singlesendpage?t=message/send&action=index&tofakeid=2302469181&token=' + token + '&lang=zh_CN'
	req2 = urllib2.Request(msgUrl,urllib.urlencode(paras2))
	req2.add_header('Accept','application/json, text/javascript, */*; q=0.01')
	req2.add_header('Accept-Encoding','gzip, deflate')
	req2.add_header('Accept-Language','en-US,en;q=0.8')
	req2.add_header('Connection','keep-alive')
	#req2.add_header('Content-Length','130')	
	req2.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
	#req2.add_header('Cookie','noticeLoginFlag=1; pgv_pvi=1648069632; data_bizuin=3075402655; data_ticket=AgVzD9024FGFJJqdeNC/QnaGAwHaBavJhzBklHevKJo=; noticeLoginFlag=1; slave_user=gh_e59bae02ed96; slave_sid=UnBITHBiMDFGQUM4WktlWUhwTnZrM2FCVzJJUlZPMHJzNDA3ajFLN0FaeUpEellLV3FTYktSVmNPU0UwWGhSTEhzSXNLdmJDeDFJek9DR3FQdjJqZlFFT3FEbGFKNkxQSmx3aUZLYVZxSXd1enRYSW1aWkRpU3pGOXdtVkxiUDA=; bizuin=3272065571')
	req2.add_header('Host','mp.weixin.qq.com')
	req2.add_header('Origin','https://mp.weixin.qq.com')
	req2.add_header('Referer',Referer)
	req2.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
	req2.add_header('X-Requested-With','XMLHttpRequest')
	ret2 = urllib2.urlopen(req2)
	print ret2.read()
	print u'消息发送成功'

#随意访问一个登陆后的页面获取ticket，用于后面构建上传图片的目标URL
def get_ticket(token):
	ticketUrl = 'https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=0&count=12&t=media/img_list&token=' + token + '&lang=zh_CN'
	Referer_ticket = 'https://mp.weixin.qq.com/cgi-bin/appmsg?begin=0&count=10&t=media/appmsg_list&type=10&action=list_card&lang=zh_CN&token=' + token
	req_ticket = urllib2.Request(ticketUrl)
	req_ticket.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	#req_ticket.add_header('Accept-Encoding','gzip, deflate, sdch')	#不要去传这个参数，否则urlopen.read()会是gzip压缩后的
	req_ticket.add_header('Accept-Language','en-US,en;q=0.8')
	req_ticket.add_header('Connection','keep-alive')
	req_ticket.add_header('Host','mp.weixin.qq.com')
	req_ticket.add_header('Referer',Referer_ticket)
	req_ticket.add_header('Upgrade-Insecure-Requests',1)
	req_ticket.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
	ret_ticket = urllib2.urlopen(req_ticket)
	page = ret_ticket.read()
	re1 = r'ticket:"(.+?)"'
	ticket_re = re.compile(re1)
	ticket = re.findall(ticket_re,page)
	print u'成功获取,ticket = ',ticket[0]
	return ticket
	
#在txt中检测图片是否已经上传过
def is_upload(path):
	fr = open('upload.txt','r')
	#return 1 for record in fr if record.strip() == path
	for record in fr:
		if record.strip() == path:
			return 1
	return 0

#上传图片
def upload_img(cj,path,ticket,token):		
	opener = poster.streaminghttp.register_openers()  
	opener.add_handler(urllib2.HTTPCookieProcessor(cj))		
	try:
		datagen,headers = multipart_encode({'file':open(path,'rb')})
	except:
		return
	#print datagen
	#print headers
	uploadUrl = 'https://mp.weixin.qq.com/cgi-bin/filetransfer?action=upload_material&f=json&writetype=doublewrite&groupid=1&ticket_id=xiuseyizhan&ticket=' + ticket + '&token=' + token + '&lang=zh_CN'
	req3 = urllib2.Request(uploadUrl,datagen,headers)
	req3.add_header('Accept','*/*')
	req3.add_header('Accept-Encoding','gzip, deflate')
	req3.add_header('Accept-Language','en-US,en;q=0.8')
	req3.add_header('Connection','keep-alive')
	#req3.add_header('Content-Length','1385')
	#req3.add_header('Content-Type','multipart/form-data; boundary=----WebKitFormBoundaryFap8PGqwcplNlhxA')
	#req3.add_header('Cookie','noticeLoginFlag=1; pgv_pvi=1648069632; noticeLoginFlag=1; data_bizuin=3075402655; data_ticket=AgVpzO8C20Hjd9sf8kIap89tAwGUiiXJsIcGa0T+qNU=; slave_user=gh_e59bae02ed96; slave_sid=ZEVxS2tINkloOUJ6Sjl2MVZoN3U4WlFLZ09aQTdKZWZrZ2ZlSUhONHJha1BXMW9vR1JBQ3VWcms2U0hibmpySENId1U5SVZ1eENIZ1B4ZmtkSkFidFdYZmx5bWF1NzVhTEdCcGpoQV9jNnBXalJOWjhIamRJcjZNRVlqMWttdUs=; bizuin=3272065571')
	req3.add_header('Host','mp.weixin.qq.com')
	req3.add_header('Origin','https://mp.weixin.qq.com')
	Referer = 'https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=0&count=12&t=media/img_list&token=' + token + '&lang=zh_CN'
	req3.add_header('Referer',Referer)
	req3.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
	while 1:
		try:
			ret3 = urllib2.urlopen(req3)
			break
		except urllib2.HTTPError,e:
			print str(e)
		except urllib2.URLError,e:
			print str(e)	
	content3 = ret3.read()
	print content3
	ret3content = json.loads(content3)	
	if ret3content['base_resp']['err_msg'] == 'ok':
		#把成功上传的文件名写入到一个txt中
		print path
		#fw = open('upload.txt','a')
		#fw.write(path.split('\\')[-2] + '\n')
		#fw.close()
		#记录下成功上传的file_id
		return ret3content['content']
	else:
		print 'upload image error %s' % path
		return 'error'

		
		
def up_pub():
	cj = cookielib.LWPCookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)

	username = {{yours}}
	pwd = {{yours}}
	token = log_in(username,pwd)
	ticket = get_ticket(token)

	#register_openers()	#这个好像是重新注册一次cookie，没有必要
	#获取图片路径
	file_name = os.listdir(os.getcwd())
	folder_name=[]
	for fn in file_name:
		if os.path.isdir(fn):
			folder_name.append(fn)

	up_list = []	#用于存储成功上传的图片的file_id
	data_ratio = []	#用于存储成功上传的图片的比例参数		
	for folder in folder_name:
		if is_upload(folder) == 0:
			#在每个文件夹下找到图片名的集合
			sub_dir = os.path.join(os.getcwd(),folder)
			img_name = os.listdir(sub_dir)
			#print img_name
			for img in img_name:
				up_dir = os.path.join(sub_dir,img)
				#print up_dir
				#横竖图片分开
				img = Image.open(up_dir)
				if img.size[1] > img.size[0]:
					file_id = upload_img(cj,up_dir,ticket[0],token)
					if file_id != 'error':
						up_list.append(file_id)
						title = up_dir.split('\\')[-2]	#读取路径的文件夹部分作为文章标题，循环读取，只有最后一个有效
						data_ratio.append('1.5')
						time.sleep(1)
			for img in img_name:
				up_dir = os.path.join(sub_dir,img)
				#print up_dir
				#横竖图片分开
				img = Image.open(up_dir)
				if img.size[1] <= img.size[0]:
					file_id = upload_img(cj,up_dir,ticket[0],token)
					if file_id != 'error':
						up_list.append(file_id)
						title = up_dir.split('\\')[-2]	#读取路径的文件夹部分作为文章标题，循环读取，只有最后一个有效
						data_ratio.append('0.66600790513834')
						time.sleep(1)

	total = len(up_list)	#本次成功上传图片总数，去构建若干URL找到图片地址
	if total != 0:
		n = total/50 + 1	#图片库页面最多可容纳50张图片
		i = 0
		up_list.reverse()
		k = 0	#记录查找的图片计数
		img_down = []	#存储找到的图片地址
		while i < n:
			begin = i * 50	
			image_page_url = 'https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=' + str(begin) + '&count=50&t=media/img_list&token=' + token + '&lang=zh_CN'
			req_image_page = urllib2.Request(image_page_url)
			#http头只添加user_agent试试
			req_image_page.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
			ret_image_page = urllib2.urlopen(req_image_page)
			image_page = ret_image_page.read()
			#找到每张图片的地址，需要up_list倒序
			j = 0	#
			while (j<50 and k<total):
				re2 = r'"file_id":%s,.+?"cdn_url":"(.+?)","img_format"' % up_list[k]
				re2_comp = re.compile(re2)
				img_down.append(re.findall(re2_comp,image_page)[0])
				j += 1
				k += 1
			i += 1
		#把\/变成/
		img_down_fix = []
		for img in img_down:
			img_down_fix.append(img.replace('\\/','/'))

		img_down_fix.reverse()
		artical_content = '<p>更多高清视频套图，尽在秀色驿站官网http://www.xiuseyizhan.com，百度搜索【秀色驿站】</p><p>          </p>'
		i = 1
		while i < total:
			down_str = '<p><img data-s=\"300,640\" data-type=\"jpeg\" data-src=\"' + img_down_fix[i] + '\" style=\"\" data-ratio=\"' + data_ratio[i] + '\" data-w=\"\"/></p>'
			artical_content += down_str
			i += 1
		artical_content += '<p><br/></p><p><br/></p>'

		
		
		#做测试，参数int和str是否影响，似乎并不影响
		artical_paras = {'token':token,'lang':'zh_CN','f':'json','ajax':1,'random':0.43593453895300627,'AppMsgId':'','count':1,'title0':title.decode('gbk','ignore').encode('utf-8'),'content0':artical_content,'digest0':' ','author0':'','fileid0':up_list[-1],'music_id0':'','video_id0':'','show_cover_pic0':1,'shortvideofileid0':'','copyright_type0':0,'can_reward0':0,'reward_wording0':'','need_open_comment0':0,'sourceurl0':'','vid':''}
		artical_url = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?t=ajax-response&sub=create&type=10&token=' + token + '&lang=zh_CN'
		Referer = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&isMul=1&isNew=1&type=10&lang=zh_CN&token=' + token
		req_artical = urllib2.Request(artical_url,urllib.urlencode(artical_paras))
		req_artical.add_header('Referer',Referer)
		req_artical.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
		ret_artical = urllib2.urlopen(req_artical)
		arti_content = ret_artical.read()
		print arti_content
		arti_dict = json.loads(arti_content)
		#返回中找到appMsgId
		appmsgid = arti_dict['appMsgId']
		print appmsgid
		#找到opreation_seq参数
		op_url = 'https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&token=' + token + '&lang=zh_CN'
		req_op = urllib2.Request(op_url)
		req_op.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
		ret_op = urllib2.urlopen(req_op)
		op_page = ret_op.read()
		re_op = r'operation_seq: "(.+?)"'
		re_op_comp = re.compile(re_op)
		operation_seq = re.findall(re_op_comp,op_page)[0]
		print operation_seq

		#去访问前一步,'direct_send':1
		#AllMsg_url = 'https://mp.weixin.qq.com/cgi-bin/masssend?t=ajax-response&token=' + token + '&lang=zh_CN' #bak 2016年1月10日之前的post URL
		AllMsg_url = 'https://mp.weixin.qq.com/cgi-bin/masssend?action=get_appmsg_copyright_stat&token=' + token + '&lang=zh_CN'
		print AllMsg_url
		#AllMsg_paras = {'token':token,'lang':'zh_CN','f':'json','ajax':1,'random':0.4500490468926728,'type':10,'appmsgid':appmsgid,'cardlimit':1,'sex':0,'groupid':-1,'synctxweibo':0,'country':'','province':'','city':'','imgcode':'','operation_seq':operation_seq} #旧的参数
		AllMsg_paras = {'token':token,'lang':'zh_CN','f':'json','ajax':1,'random':0.5902709965594113,'first_check':1,'type':10,'appmsgid':appmsgid}
		print urllib.urlencode(AllMsg_paras)
		Referer = 'https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&token=' + token + '&lang=zh_CN'
		req_am = urllib2.Request(AllMsg_url,urllib.urlencode(AllMsg_paras))
		req_am.add_header('Accept','application/json, text/javascript, */*; q=0.01')
		req_am.add_header('Accept-Encoding','gzip, deflate')
		req_am.add_header('Accept-Language','zh-CN,zh;q=0.8')
		req_am.add_header('Connection','keep-alive')
		req_am.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
		req_am.add_header('Host','mp.weixin.qq.com')
		req_am.add_header('Origin','https://mp.weixin.qq.com')
		req_am.add_header('Referer',Referer)
		req_am.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
		req_am.add_header('X-Requested-With','XMLHttpRequest')
		ret_am = urllib2.urlopen(req_am)
		new_final = ret_am.read()
		print new_final
		new_final_dict = json.loads(new_final)
		
		#2015年11月6的更新，只用往那个地址发送一次请求就能成功发送文章了，new_final_dict
		#我猜测是要分两步，应该要成功了

		AllMsg_url = 'https://mp.weixin.qq.com/cgi-bin/masssend?action=get_appmsg_copyright_stat&token=' + token + '&lang=zh_CN'
		#AllMsg_paras = {'token':token,'lang':'zh_CN','f':'json','ajax':1,'random':0.4500490468926728,'type':10,'appmsgid':appmsgid,'cardlimit':1,'sex':0,'groupid':-1,'synctxweibo':0,'country':'','province':'','city':'','imgcode':'','operation_seq':operation_seq,'direct_send':1}
		AllMsg_paras = {'token':token,'lang':'zh_CN','f':'json','ajax':1,'random':0.8302679362241179,'first_check':0,'type':10,'appmsgid':appmsgid}
		print urllib.urlencode(AllMsg_paras)
		Referer = 'https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&token=' + token + '&lang=zh_CN'
		req_am = urllib2.Request(AllMsg_url,urllib.urlencode(AllMsg_paras))
		req_am.add_header('Accept','application/json, text/javascript, */*; q=0.01')
		req_am.add_header('Accept-Encoding','gzip, deflate')
		req_am.add_header('Accept-Language','zh-CN,zh;q=0.8')
		req_am.add_header('Connection','keep-alive')
		req_am.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
		req_am.add_header('Host','mp.weixin.qq.com')
		req_am.add_header('Origin','https://mp.weixin.qq.com')
		req_am.add_header('Referer',Referer)
		req_am.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
		req_am.add_header('X-Requested-With','XMLHttpRequest')
		ret_am = urllib2.urlopen(req_am)
		final = ret_am.read()
		print final	
		final_dict = json.loads(final)
		
		#2016年1月10日改版后，抓包显示有3个post，全部模拟出来
		AllMsg_url = 'https://mp.weixin.qq.com/cgi-bin/masssend?t=ajax-response&token=' + token + '&lang=zh_CN' #bak 2016年1月10日之前的post URL
		AllMsg_paras = {'token':token,'lang':'zh_CN','f':'json','ajax':1,'random':0.7723801680840552,'type':10,'appmsgid':appmsgid,'cardlimit':1,'sex':0,'groupid':-1,'synctxweibo':0,'country':'','province':'','city':'','imgcode':'','operation_seq':operation_seq,'direct_send':1} #旧的参数
		print urllib.urlencode(AllMsg_paras)
		Referer = 'https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&token=' + token + '&lang=zh_CN'
		req_am = urllib2.Request(AllMsg_url,urllib.urlencode(AllMsg_paras))
		req_am.add_header('Accept','application/json, text/javascript, */*; q=0.01')
		req_am.add_header('Accept-Encoding','gzip, deflate')
		req_am.add_header('Accept-Language','zh-CN,zh;q=0.8')
		req_am.add_header('Connection','keep-alive')
		req_am.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
		req_am.add_header('Host','mp.weixin.qq.com')
		req_am.add_header('Origin','https://mp.weixin.qq.com')
		req_am.add_header('Referer',Referer)
		req_am.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36')
		req_am.add_header('X-Requested-With','XMLHttpRequest')
		ret_am = urllib2.urlopen(req_am)
		new_final = ret_am.read()
		print new_final
		new_final_dict = json.loads(new_final)
		
		if new_final_dict['base_resp']['err_msg'] == 'ok':
			#把title写入release.txt
			fw = open('released.txt','a')
			fw.write(title + '\n')
			fw.close()
			#把title写入upload.txt
			fw = open('upload.txt','a')
			fw.write(title + '\n')
			fw.close()
	else:
		print u'没有新素材发布'
		
def up_pub_try():
	try:
		up_pub()
		return 1
	except:
		return 0
		
if __name__=='__main__':
	up_pub()