# -*- coding:utf-8 -*-

import qiniu
import os
import re
import urllib
import urllib2
import cookielib
import json
from poster.encode import multipart_encode,MultipartParam
from poster.streaminghttp import register_openers
import requests
import poster
import time
from PIL import Image
import socket
import sys

def qn_up_img(file_path,uped_name):
    qiniu_access_key = {{your}}
    qiniu_secret_key = {{your}}
    qiniu_bucket_name = "xiuseyizhan"

    q = qiniu.Auth(qiniu_access_key,qiniu_secret_key)
    key = uped_name
    mime_type = "image/jpeg"
    params = {'x:a': 'a'}
    localfile = file_path

    token = q.upload_token(qiniu_bucket_name, key)
    ret, info = qiniu.put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
    #print info
    assert ret['key'] == key
    assert ret['hash'] == qiniu.etag(localfile)

def log_in(username,pwd,csrfmiddlewaretoken):
    paras = {'username':username,'password':pwd,'csrfmiddlewaretoken':csrfmiddlewaretoken,'next':'/admin/'}
    req = urllib2.Request('http://121.42.175.88/admin/login/?next=/admin/',urllib.urlencode(paras))
    #req.add_header('Accept','*/*')
    #req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header('Accept-Language','zh-CN,zh;q=0.8')
    req.add_header('Connection','keep-alive')
    #req.add_header('Content-Length','79')
    req.add_header('Content-Type','application/x-www-form-urlencoded')
    #req.add_header('Cookie','noticeLoginFlag=1; pgv_pvi=1648069632; noticeLoginFlag=1')
    req.add_header('Host','121.42.175.88')
    req.add_header('Origin','http://121.42.175.88')
    req.add_header('Referer','http://121.42.175.88/admin/login/?next=/admin/')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
    #req.add_header('X-Requested-With','XMLHttpRequest')
    ret = urllib2.urlopen(req)

#获取django管理后台的csrftoken
def get_csrf(url):
    rep = urllib2.urlopen(url)
    log_page = rep.read()
    re_csrf = re.compile(r"name='csrfmiddlewaretoken' value='(.+?)'")
    csrfmiddlewaretoken = re.search(re_csrf,log_page).group(1)
    return csrfmiddlewaretoken

def post_article(params): 
    #绑定cookie，自动处理cookie
    cj = cookielib.LWPCookieJar()
    #生成一个带cookie的opener，可以使用opener.open()打开URL
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #安装opener，使得可以直接用urllib2.urlopen()带上cookie
    urllib2.install_opener(opener)
    #获取csrfmiddlewaretoken
    csrfmiddlewaretoken = get_csrf('http://121.42.175.88/admin/login/?next=/admin/')
    username = {{yours}}
    pwd = {{yours}}
    log_in(username,pwd,csrfmiddlewaretoken)

    #获取add页面的csrf
    csrfmiddlewaretoken = get_csrf('http://121.42.175.88/admin/blog/article/add/')

    params['csrfmiddlewaretoken'] = csrfmiddlewaretoken
    
    #print params

    items = []
    for key,value in params.items():
        items.append(MultipartParam(key,value))

    opener = poster.streaminghttp.register_openers()  
    opener.add_handler(urllib2.HTTPCookieProcessor(cj))
        
    #这里只有name-value对，直接用dict就可以成功
    #stackflow上提到如果上传键值对和文件，键值对先要封装成MultipartParam类
    #这里我持怀疑态度，官方说MultipartParam类处理独立的一对键值对
    #这里使用封装后的items也可以的
    datagen, headers = multipart_encode(params)


    additionalHeaders = {
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'121.42.175.88',
        'Origin':'http://121.42.175.88',
        'Referer':'http://121.42.175.88/admin/blog/article/add/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    }

    for key,value in additionalHeaders.iteritems():
        headers[key] = value
     
    req = urllib2.Request('http://121.42.175.88/admin/blog/article/add/', datagen, headers)

    ret = urllib2.urlopen(req)

def up_pub():
    re_inst = r'No.(\d+?)\D'
    re_inst = re.compile(re_inst)
    re_date = r'\d{4}\.\d{2}\.\d{2}'
    re_date = re.compile(re_date)

    img_folders = 'c:/upload_web/'
    for folder in os.listdir(img_folders):
        folder_path = os.path.join(img_folders,folder)
        if os.path.isdir(folder_path):
            #folder应该是gbk编码，re_inst是utf-8编码，但是还是能匹配出数字，我以前匹配中文是都转的unicode
            inst = re.search(re_inst,folder).group(1)
            print inst
            imgs = os.listdir(folder_path)
            #找到套图发布日期
            pub_date = re.search(re_date,folder).group()
            #把图片按长宽比例分为两类
            img_groupA = []
            img_groupB = []
            for img in imgs:
                img_path = os.path.join(folder_path,img)
                uped_img = (folder+'_'+img).decode('GBK')            
                print u'正在上传 ',uped_img
                uped_name = 'beautyleg_p_'+inst+'_'+img
                qn_up_img(img_path,uped_name)
                
                img_s = Image.open(img_path)
                if img_s.size[1] > img_s.size[0]:
                    img_groupA.append(uped_name)
                else:
                    img_groupB.append(uped_name)
            #上传完一个文件夹就发布一篇文章
            title = folder.decode('GBK').encode('utf-8')
            en_title = 'beautyleg_p_' + inst.decode('GBK').encode('utf-8')
            img = 'http://7xpgaf.com1.z0.glb.clouddn.com/' + img_groupB[0] + '?imageMogr2/thumbnail/621x621'
            pub_time_0 = pub_date.replace('.','/')
            #算出content
            content = '<div class="baguetteBoxOne gallery">'
            for uped_name in img_groupA:
                herf1 = 'http://7xpgaf.com1.z0.glb.clouddn.com/' + uped_name
                herf2 = herf1 + '?imageMogr2/thumbnail/!210x210r/gravity/Center/crop/210x210'
                tag_a = '<a href="%s"><img src="%s" width="33.3%%"></a>' % (herf1,herf2)
                content += tag_a
            for uped_name in img_groupB:
                herf1 = 'http://7xpgaf.com1.z0.glb.clouddn.com/' + uped_name
                herf2 = herf1 + '?imageMogr2/thumbnail/!210x210r/gravity/Center/crop/210x210'
                tag_a = '<a href="%s"><img src="%s" width="33.3%%"></a>' % (herf1,herf2)
                content += tag_a
            content += '</div>'
            #一些上传params的常量
            category = '1'
            tags = ''
            author = '1'
            rank = '0'
            status = '0'
            summary = ''
            pub_time_1 = '12:34'
            _save = '保存'
            params = {
                'title':title, #folder
                'en_title':en_title, #'beautyleg_p_'+inst
                'img':img, #第一张横放的照片做封面
                'category':'1', 
                'tags':'',
                'author':'1',
                'rank':'0',
                'status':'0',
                'content':content,
                'summary':'',
                'pub_time_0':pub_time_0,  #匹配出发布时间
                'pub_time_1':'13:59',
                '_save':'保存'
            }
            #调用发文章接口
            post_article(params)

if __name__ == '__main__':
    up_pub()
    

