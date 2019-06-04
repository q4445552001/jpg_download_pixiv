import requests
import re
import http.cookiejar
from http import cookies

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}

datas = {
    'pixiv_id': 'moe1user',
    'password': '630489372',
    'captcha': '',
    'g_reaptcha_response': '',
    'post_key': '',
    'source': 'pc',
    'ref': 'wwwtop_accounts_indes',
    'return_to': 'https://www.pixiv.net/'
}

LOGIN_URL = 'https://accounts.pixiv.net/login'
POST_URL = 'https://accounts.pixiv.net/api/login?lang=en'

def resetcookie(session,s):
	cookies = {}
	for seq in s.split(';'):
		if seq.find('=') != -1:
			key,value=seq.split('=',1)
			if key == 'PHPSESSID':
				cookies[key]=value
				break
	return cookies

s=requests.Session()
s.headers = headers

loginPage = s.get(LOGIN_URL)

datas['post_key'] = re.compile(r'name="post_key" value="(.*?)">').findall(loginPage.text)[0]

response=s.post(POST_URL,data=datas)
return_data=resetcookie(s,response.headers['set-cookie'])