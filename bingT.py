#coding=utf-8
import urllib
import json
import time
import datetime
import os
from qiniu import Auth, put_data, put_file

save_path ='g:\\bingimg\\'  #本地保存路径，修改为自己的
access_key = '' #七牛ak，修改为自己的
secret_key = '' #七牛sk，修改为自己的
bucket_name = ''  #七牛保存空间名，修改为自己的
pass_day=1 #获取过去几天的数据，最多19，最小1相当于获取当天数据

def getUrl(path):
     for i in range(0,1):
          rand_key =str(time.time()).split('.')[0]
          page = urllib.urlopen("http://cn.bing.com/HPImageArchive.aspx?format=js&idx=%s&n=1&nc=%s&pid=hp" %(i,rand_key))
          jData = page.read()
          if jData.strip() =='':
               continue
          data = json.loads(jData)
          print '-------------------------'
          imgurl = data['images'][0]['url']
          if imgurl.strip() =='':
               continue
          index = imgurl.index('.')
          if index<=0:
               continue
          imArry= imgurl.split('.')
          img_type = imArry[-1]
          now = datetime.datetime.now()
          otherStyleTime = now.strftime("%Y-%m-%d")
          file_path = str('%s%s_%s.%s' %(path,otherStyleTime,i,img_type))
          urllib.urlretrieve(imgurl,file_path)
          #上传到七牛云存储
          uploadToQiNiu(file_path,str('%s_%s.%s' %(otherStyleTime,i,img_type) ))
          
def uploadToQiNiu(filePath,name):
     q = Auth(access_key, secret_key)
     localfile = filePath
     key = name
     mime_type = "image/jpeg"
     token = q.upload_token(bucket_name, key)
     ret, info = put_file(token, key, localfile, mime_type=mime_type, check_crc=True)

getUrl(save_path)
