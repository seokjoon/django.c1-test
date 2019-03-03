from bs4 import BeautifulSoup
from selenium import webdriver
import requests

from time import sleep
from datetime import datetime
from multiprocessing import Pool

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p1.settings')
django.setup()
from a1.models import App


def getApp(pkg):
	html = requests.get('https://play.google.com/store/apps/details?id=' + pkg).text
	soup = BeautifulSoup(html, 'html.parser')
	infos = soup.select('c-wiz > div > div > div > div > span > div > span.htlgb')
	info_mail = soup.select('c-wiz > div > div > div > div > span > div > span.htlgb > div > a')
	# info_title = soup.select_one('c-wiz > h1 > span')
	# print(infos)

	titles = {1: 'date', 3: 'installed', 7: 'provider', 8: 'mail'}
	outs = {'pkg': pkg}
	i = 1
	for info in infos:
		title = titles.get(i)
		if title == 'mail':
			outs[title] = info_mail[1].text
		elif title:
			outs[title] = info.text
		i = i + 1
	# print(pkg)
	# print(outs)
	return outs


def getApps():
	# driver = webdriver.Chrome('/Volumes/data/ws.noSync/app2/j1/lib/webdriver/chrome/chromedriver')
	driver = webdriver.PhantomJS('/Volumes/data/ws.noSync/app2/j1/lib/webdriver/phantomjs/phantomjs/bin/phantomjs')
	# driver.implicitly_wait(3)
	driver.get('https://play.google.com/store/search?q=%EC%86%90%EC%A0%84%EB%93%B1&c=apps')

	i, height = (0,) * 2
	# while i < 10:
	while i < 1:
		driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
		height_new = driver.execute_script('return document.body.scrollHeight')
		if height == height_new:
			break
		height = height_new
		sleep(2)
		btn_more = driver.find_element_by_id('show-more-button')
		if btn_more.text:
			btn_more.click()
		i = i + 1
		# print(str(i) + ':' + str(height))

	outs = {}
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	apps = soup.select('div.details > a.title')
	for app in apps:
		outs[app.get('href').split('id=')[1]] = app.text

	return outs


# if __name__=='__main__':
apps = getApps()
pool = Pool(processes=4)
appsData = pool.map(getApp, apps.keys())
# appsData = pool.map(apps.keys(), getApp())
# print(appsData)
i = 0
for p, t in apps.items():
	data = appsData[i]
	i = i + 1
	try: d = datetime.strptime(data['date'].replace(',', ''), '%B %d %Y').date()
	except: d = datetime.now().date()
	installed = data['installed'].replace(',', '').replace('+', '').replace('.', '').replace('M', '000000') # FIXME
	modified = datetime.now().isoformat()[0:10]
	try: App(pkg=p, title=t, date=d, modified=modified, installed=installed, provider=data['provider'], mail=data['mail']).save()
	except: continue # print(data) # FIXME
print(appsData)
