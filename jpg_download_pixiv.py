#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests,os,time,json
from bs4 import BeautifulSoup
from collections import OrderedDict
import cookies

path = '/mnt/hgfs/Download/Image/img/'
dir = 'pixiv'

f = open('./jpg_download_pixiv.txt','r')
for line in f.readlines():
	list = line.split(',')
f.close

def getsoup(url):
		webside = requests.get(url,cookies = cookies.return_data)
		soup = json.loads(BeautifulSoup((webside.text).encode('utf-8'), 'html.parser').text, object_pairs_hook = OrderedDict)
		return soup

timesum = 0
for id in list:
	if id :
		img_urls = []
		
		start = time.time() #時間開始
		print id + ' Check Start'

		if (os.path.isdir(path + dir + "/" + id) == True):
			stopimg = os.popen("ls " + path + dir + "/" + id + " | tail -n 1").read().split("_")[0] #擷取資料夾最後一個檔案
		else:
			stopimg = ''

		#取得 ID 作品頁面
		soup = getsoup('https://www.pixiv.net/ajax/user/' + id + '/profile/all')
		for key, value in soup['body']['illusts'].items():
			if stopimg :
				if key <= stopimg :
					break
			
		try:
			#取得圖片下載網址
			soup = getsoup('https://api.imjad.cn/pixiv/v2/?id=' + key)

			if soup['illust']['type'] == 'illust':
				if soup['illust']['meta_pages']:	
					count = 0
					for li in soup['illust']['meta_pages']:
						img_urls.append(soup['illust']['meta_pages'][count]['image_urls']['original'])
						count += 1
				else:
					img_urls.append(soup['illust']['meta_single_page']['original_image_url'])
			#動圖下載
			elif soup['illust']['type'] == 'ugoira':
				img_urls.append('https://i.pximg.net/img-zip-ugoira' + soup['illust']['meta_single_page']['original_image_url'].replace('\\','').split('img-original')[1].split('_')[0] + '_ugoira1920x1080.zip')
		
		except Exception, echo:
			print key + ' ERROR'
			os.system("touch %s"%(path) + "pixiv_error.txt")
			file = open(path + "pixiv_error.txt","a+")
			file.writelines(str(echo) + ': ' + key + ' ERROR\n')
			file.close()
				
		for img_url in img_urls:
			os.system("wget -q -nc --show-progress --referer='http://www.pixiv.net/' -t 5 -T 30 -P " + path + dir + "/" + id + " " + img_url)

		end = time.time() #時間結束
		timelog = end - start #花費時間
		print id + ' Check End. Time consuming : ' + str(timelog) + ' sec'
		timesum = timesum + timelog

print "Time Sum : " + str(timesum/60) + ' min'