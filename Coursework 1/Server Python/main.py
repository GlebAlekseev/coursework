import requests
import bs4
from threading import Thread
import datetime
import logging

import os
import json
import platform
from selenium import webdriver
import logging
from seleniumwire import webdriver  
import json
from fake_headers import Headers
import sqlite3
#Линки с магазинами на поиск
import urllib3
import certifi
import urllib.parse
Links_storage = {'Wildberries': ['https://wbxsearch.wildberries.ru/exactmatch/v2/common?query=REQUEST&_app-type=sitemobile',
								 'https://wbxcatalog-ru.wildberries.ru/BUCKET/catalog?PRESET&appType=2&spp=0&regions=68,75,69,40,48,33,70,64,1,4,38,30,71,22,31,66&stores=119261,122252,122256,117673,122258,122259,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124093,124094,124095,124096,124097,124098,124099,124100,124101,120762,119400,116433,507,3158,120602,6158,117501,121709,2737,117986,1699,1733,686,117413,119070,118106,119781&pricemarginCoeff=1&pricemarginMin=0&pricemarginMax=0&reg=0&emp=0&lang=ru&locale=ru&version=3&curr=rub&page=PAGE',
								 'https://wbxcatalog-ru.wildberries.ru/SHARD/catalog?SUBJECT&search=NAME&page=PAGE&appType=2&spp=0&regions=68,75,69,40,48,33,70,64,1,4,38,30,71,22,31,66&stores=119261,122252,122256,117673,122258,122259,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124093,124094,124095,124096,124097,124098,124099,124100,124101,120762,119400,116433,507,3158,120602,6158,117501,121709,2737,117986,1699,1733,686,117413,119070,118106,119781&pricemarginCoeff=1&pricemarginMin=0&pricemarginMax=0&reg=0&emp=0&lang=ru&locale=ru&version=3&curr=rub'],
				 'my-shop':		['http://my-shop.ru/cgi-bin/shop2.pl?q=search&sort=z&page=PAGE&f14_6=REQUEST',
					  	    	 'https://my-shop.ru/cgi-bin/shop2.pl?q=product&id=3143442'],
				 'eldorado':	['https://www.eldorado.ru/sem/v3/a408/products?rootRestrictedCategoryId=0&query=REQUEST&orderField=popular&limit=50&offset=PAGE&regionId=11324',
								 'https://api.retailrocket.net/api/1.0/partner/5ba1feda97a5252320437f20/items/?itemsIds=71112985&stock=&format=json'],
				 'aliexpress':	['https://aliexpress.ru/glosearch/api/product?trafficChannel=main&d=y&CatId=0&SearchText=REQUEST&ltype=wholesale&SortType=default&page=PAGE&origin=y']
					  	    	 }
					  	    	 # Wildberries 100
					  	    	 # my-shop 36
					  	    	 # eldorado 50
					  	    	 # aliexpress 60

#Поисковой запрос 
start =datetime.datetime.now()
connect = sqlite3.connect("data.db") # или :memory: чтобы сохранить в RAM
connect.isolation_level= 'DEFERRED'
connect.execute('''PRAGMA synchronous = OFF''')
connect.execute('''PRAGMA journal_mode = OFF''')
# connect = sqlite3.connect(":memory:")
cursor = connect.cursor()

try:
	cursor.execute("""CREATE TABLE items
                  (id text, subjectid text, name text, brand text, brandId text, sale text, priceU text, salePriceU text, pics text, rating text, feedbacks text, history text,last_history text )
               """)
except sqlite3.OperationalError:
	print("БД уже создана")
else:
	print("Создание БД")
# Подогнать бд


class Create_a_database_based_on_the_search_query:
	def __init__(self,request_name,links_storage = Links_storage):
		self.request_name = request_name
		self.links_storage = links_storage
		self.session = requests.Session()
		headers= Headers(
        browser="chrome",
        os="win", 
        headers=True 
    	)
		# self.session.headers = {
		# 	'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Mobile Safari/537.36',
		# 	'Accept': 'application/json',
		# 	'accept-language':'ru',


		# }

		self.session.headers = headers.generate()
		self.pages = 1
		self.result = []

	def WildBerries_add(self,a):
		newurl = self.links_storage['Wildberries'][0].replace("REQUEST",str(self.request_name))
		res = self.session.get(url=newurl)
		res.raise_for_status()
		data_find_filters_decode = []
		data_find_filters_decode = json.loads(res.text)
		if len(data_find_filters_decode) == 0: # Пустой ответ от Wildberries
			print("Ничего не найдено")
		else:
			i=0
			while i<20:
				staTime = datetime.datetime.now()
				print('Страница ', i)
				if data_find_filters_decode["query"].find("subject=") != -1:
					newurl = self.links_storage['Wildberries'][2].replace("PAGE",str(i+1)).replace("SHARD",str(data_find_filters_decode["shardKey"])).replace("SUBJECT",str(data_find_filters_decode["query"])).replace("NAME",str(data_find_filters_decode["name"]))
				elif data_find_filters_decode["query"].find("preset=") != -1:
					newurl = self.links_storage['Wildberries'][1].replace("PAGE",str(i+1)).replace("BUCKET",str(data_find_filters_decode["shardKey"])).replace("PRESET",str(data_find_filters_decode["query"]))
				res = self.session.get(url=newurl)
				res.raise_for_status()
				data_decode = []
				data_decode = json.loads(res.text)
				last_history = str(datetime.datetime.now()) + ';'
				if len(data_decode['data']['products']) == 0:
					break
				for item in data_decode['data']['products']:
					# Проверка на наличие, если есть то обновляет цену скидка отзывы и тд, обновляет историю плюсуя к старой, а в конец дает сегодняшнюю
					info = cursor.execute('SELECT * FROM items WHERE id=?', (item["id"], ))
					if info.fetchone() is None: 
							#Делаем когда нету человека в бд
							history = last_history
							data = (item["id"], item["subjectId"],item["name"],item["brand"],item["brandId"],item["sale"],item["priceU"],item["salePriceU"],item["pics"],item["rating"],item["feedbacks"],history,last_history) 
							# Вставляем данные в таблицу
							cursor.execute("INSERT INTO items VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
					else:
							#Делаем когда есть человек в бд
							info = cursor.execute('SELECT * FROM items WHERE id=?', (item["id"], ))
							records = cursor.fetchall()
							history = str(records[0]).replace('(','').replace(')','').split(',') # Добавить историю цен
							history = history[11].replace("'",'').strip() + '\n' + last_history
							cursor.execute('UPDATE items SET sale = ?,  priceU = ?,salePriceU = ?,rating = ?,feedbacks = ?,history = ?,last_history = ? WHERE id = ?',( item["sale"],item["priceU"],item["salePriceU"],item["rating"],item["feedbacks"],history,last_history,item["id"], ))
				i+=1



	def myShop_add(self,a): # Добавить доп ячейки и добав в БД
		i=0
		newurl = self.links_storage['my-shop'][0].replace("REQUEST",urllib.parse.quote(str(self.request_name)))
		http = urllib3.PoolManager(ca_certs=certifi.where())
		payload = {'f14_6': self.request_name}
		encoded_data = json.dumps(payload).encode('utf-8')
		bodyM = urllib.parse.quote(str(self.request_name))
		while i<10:
			print('Страница ', i)
			newurl_In = newurl.replace("PAGE",str(i+1))
			resp = http.request(
				'POST',
				newurl_In,
				body=encoded_data,
				headers={'Content-Type': 'application/json'})
			data = json.loads(resp.data.decode('utf-8'))
			for item in data['products']:
				print(item['product_id'],item['cost'],item['title'],item['ga_item']['id'],item['ga_item']['brand'])

			i+=1

	def Eldorado_add(self,a): # Добавить доп ячейки и добав в БД
			newurl = self.links_storage['eldorado'][0].replace("REQUEST",str(self.request_name))
			i=0
			while i<20:

				newurl_In = newurl.replace("PAGE",str(i*50))
				# print(newurl_In)
				res = self.session.get(url=newurl_In)
				res.raise_for_status()
				data_find_filters_decode = []
				data_find_filters_decode = json.loads(res.text)
				print('Страница ', i)


				for item in data_find_filters_decode['data']:
					print(item['id'],item['name'],item['shortName'],item['productId'],item['brandName'],item['price'],item['oldPrice'],item['rating'])


				i+=1


		# for block in data:
		# 	print("-----------########",data)
		# data_find_filters_decode = []
		# data_find_filters_decode = json.loads(res.text)
		# print(data_find_filters_decode)

		# if len(data_find_filters_decode) == 0: # Пустой ответ от Wildberries
		# 	print("Ничего не найдено")
		# else:
		# 	i=0
		# 	while i<20:
		# 		staTime = datetime.datetime.now()
		# 		print('Страница ', i)
		# 		if data_find_filters_decode["query"].find("subject=") != -1:
		# 			newurl = self.links_storage['Wildberries'][2].replace("PAGE",str(i+1)).replace("SHARD",str(data_find_filters_decode["shardKey"])).replace("SUBJECT",str(data_find_filters_decode["query"])).replace("NAME",str(data_find_filters_decode["name"]))
		# 		elif data_find_filters_decode["query"].find("preset=") != -1:
		# 			newurl = self.links_storage['Wildberries'][1].replace("PAGE",str(i+1)).replace("BUCKET",str(data_find_filters_decode["shardKey"])).replace("PRESET",str(data_find_filters_decode["query"]))
		# 		res = self.session.get(url=newurl)
		# 		res.raise_for_status()
		# 		data_decode = []
		# 		data_decode = json.loads(res.text)
		# 		last_history = str(datetime.datetime.now()) + ';'
		# 		if len(data_decode['data']['products']) == 0:
		# 			break
		# 		for item in data_decode['data']['products']:
		# 			# Проверка на наличие, если есть то обновляет цену скидка отзывы и тд, обновляет историю плюсуя к старой, а в конец дает сегодняшнюю
		# 			info = cursor.execute('SELECT * FROM items WHERE id=?', (item["id"], ))
		# 			if info.fetchone() is None: 
		# 					#Делаем когда нету человека в бд
		# 					history = last_history
		# 					data = (item["id"], item["subjectId"],item["name"],item["brand"],item["brandId"],item["sale"],item["priceU"],item["salePriceU"],item["pics"],item["rating"],item["feedbacks"],history,last_history) 
		# 					# Вставляем данные в таблицу
		# 					cursor.execute("INSERT INTO items VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
		# 			else:
		# 					#Делаем когда есть человек в бд
		# 					info = cursor.execute('SELECT * FROM items WHERE id=?', (item["id"], ))
		# 					records = cursor.fetchall()
		# 					history = str(records[0]).replace('(','').replace(')','').split(',') # Добавить историю цен
		# 					history = history[11].replace("'",'').strip() + '\n' + last_history
		# 					cursor.execute('UPDATE items SET sale = ?,  priceU = ?,salePriceU = ?,rating = ?,feedbacks = ?,history = ?,last_history = ? WHERE id = ?',( item["sale"],item["priceU"],item["salePriceU"],item["rating"],item["feedbacks"],history,last_history,item["id"], ))
		# 		i+=1









	def search_start(self): # Разбить на потоки, добавить или убрать алик, решить проблему с поштучной проверкой
		self.WildBerries_add(1)
		self.myShop_add(1)
		self.Eldorado_add(1)
		# WildBerries = Thread(target=self.WildBerries_add, args=(1, ))
		# WildBerries.start()
		# Разные магазины ... 
		connect.commit()
		print("commit")



		# ТЕСТ ЗАПРОСЫ
Create_a_database_based_on_the_search_query('Крем').search_start()
# Create_a_database_based_on_the_search_query('Поиск').search_start()
# Create_a_database_based_on_the_search_query('Машина').search_start()
# Create_a_database_based_on_the_search_query('а').search_start()
# Create_a_database_based_on_the_search_query('оружие').search_start()
# Create_a_database_based_on_the_search_query('стрельба').search_start()
# Create_a_database_based_on_the_search_query('книга').search_start()
print('end')
print('Завершил сеанс за ', (datetime.datetime.now() - start))
	# def Get_fullLink(self):

	# 	chromedriver_path = 'C:\swdriver\chromedriver.exe'
	# 	options = webdriver.ChromeOptions()
	# 	options.add_argument('headless')
	# 	driver = webdriver.Chrome(executable_path = chromedriver_path,chrome_options=options)
	# 	driver.get(self.links_storage)

# 		self.request = request
# 		self.session = requests.Session() # записывает кукисы заголовки, антиподозрение
# 		self.session.headers = {
# 			'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Mobile Safari/537.36',
# 			'accept-language':'ru',
# 		}
# 		self.pages = 1
# 		self.result = []


# massive = []
# # Access requests via the `requests` attribute
# print('start')
# for request in driver.requests:
# 	if request.response:
# 		# if request.url.find('https://wbxcatalog-ru.wildberries.ru/') != -1:
# 		# print(request.response.body.decode())
# 		# print(request.response.status_code)
# 		# print(request.response.headers['Content-Type'])
# 		# massive.append(request.response.body)
# 		massive.append(request.url)

# with open('out.txt', 'w', encoding='utf-8') as fp:# собираем то, что в файл попадет(data), +имя фйала(filename)+ расширение, открываем неа запись(w)
# 	print(massive, file=fp, sep="\n")# запись в файл с переводом строки
# 	fp.close()# закрытие файла




# # Link, Название 1, Название 2, Картинку (link), Цена, Цена со скидкой, Отзывов, Рейтинг(звезд) - Wildberries
# #  - Ozon
# # Aliexpress
# # DNS
# # Citilink 'https://www.wildberries.ru/catalog/0/search.aspx?search=REQUEST&page=PAGE',
# Links_storage = ['https://www.wildberries.ru/catalog/0/search.aspx?search=REQUEST&page=PAGE',
# 				 'https://www.dns-shop.ru/search/?q=REQUEST&p=PAGE',
# 				 'https://www.ozon.ru/search/?from_global=true&page=PAGE&text=REQUEST',
# 				 'https://aliexpress.ru/wholesale?trafficChannel=main&d=y&CatId=0&SearchText=REQUEST&ltype=wholesale&SortType=default&page=PAGE',
# 				 'https://aliexpress.ru/wholesale?catId=0&SearchText=крем&page=1',
# 				 'https://www.citilink.ru/search/?text=REQUEST&p=PAGE']

# # 5 функций распарса



# # def Ozon_potoks(url,self,j):
# # 	for i in range(2):
# # 		temp_time_start = datetime.datetime.now()
# # 		newurl = url.replace("PAGE",str(j+i))
# # 		res = self.session.get(url=newurl)
# # 		# res.raise_for_status()
			
# # 		soup = bs4.BeautifulSoup(res.text, 'lxml')
# # 		container = soup.select('div.a0c6.a0c9')
# # 		temp_time_end = datetime.datetime.now()
# # 		print(container)
# # 		print(j+i," завершил за",(temp_time_end-temp_time_start).microseconds)
# # def Get_data_Ozon(self,request_words,pages=10):
# # 	global Links_storage
# # 	url = Links_storage[2].replace("REQUEST",request_words)
# # 	j=0
# # 	while j<pages:
# # 		thred_Ozon_on_pages = Thread(target=Ozon_potoks, args=(url,self,j, ))
# # 		thred_Ozon_on_pages.start()
# # 		j +=2







# # def Citilink_potoks(url,self,j):
# # 	for i in range(2):
# # 		temp_time_start = datetime.datetime.now()
# # 		newurl = url.replace("PAGE",str(j+i))
# # 		res = self.session.get(url=newurl)
# # 		# res.raise_for_status()
			
# # 		soup = bs4.BeautifulSoup(res.text, 'lxml')
# # 		container = soup.select('div.product_data__gtm-js.product_data__pageevents-js.ProductCardVertical.js--ProductCardInListing.ProductCardVertical_normal.ProductCardVertical_shadow-hover.ProductCardVertical_separated')
# # 		temp_time_end = datetime.datetime.now()
# # 		# print(container)


# # 		with open("out.json", "w") as write_file:
# # 			json.dump(container, write_file, indent=2)



# # 		print(j+i," завершил за",(temp_time_end-temp_time_start).microseconds)
# # def Get_data_Citilink(self,request_words,pages=10):
# # 	global Links_storage
# # 	url = Links_storage[4].replace("REQUEST",request_words)
# # 	j=0
# # 	while j<pages:
# # 		thred_Citilink_on_pages = Thread(target=Citilink_potoks, args=(url,self,j, ))
# # 		thred_Citilink_on_pages.start()
# # 		j +=


# def Wild_potoks(url,self,j):
# 	for i in range(1):
# 		temp_time_start = datetime.datetime.now()
# 		newurl = url.replace("PAGE",str(j+i))
# 		res = self.session.get(url=newurl)
# 		# res.raise_for_status()
			
# 		soup = bs4.BeautifulSoup(res.text, 'lxml')
# 		# container = soup.select('div._3UXcY')
# 		container = soup.select('body')
# 		temp_time_end = datetime.datetime.now()
# 		with open('out.txt', 'w', encoding='utf-8') as fp:# собираем то, что в файл попадет(data), +имя фйала(filename)+ расширение, открываем неа запись(w)
# 			print(container, file=fp, sep="\n")# запись в файл с переводом строки
# 			fp.close()# закрытие файла

# 		# print(j+i," завершил за",(temp_time_end-temp_time_start).microseconds)
# def Get_data_WildBerries(self,request_words,pages=10):
# 	global Links_storage
# 	url = Links_storage[0].replace("REQUEST",request_words)
# 	j=0
# 	while j<pages:
# 		thred_wild_on_pages = Thread(target=Wild_potoks, args=(url,self,j, ))
# 		thred_wild_on_pages.start()
# 		j +=1
# # Запускается отдельный поток на пользователя
# class FormingDataForRequest:
# 	def __init__(self,request):
# 		self.request = request
# 		self.session = requests.Session() # записывает кукисы заголовки, антиподозрение
# 		self.session.headers = {
# 			'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Mobile Safari/537.36',
# 			'accept-language':'ru',
# 		}
# 		self.pages = 1
# 		self.result = []

# 	def run(self):
# 		WildBerries = Thread(target=Get_data_WildBerries, args=(self,self.request,self.pages, ))
# 		# Ozon = Thread(target=Get_data_Ozon, args=(self,self.request,self.pages, ))
# 		# Citilink = Thread(target=Get_data_Citilink, args=(self,self.request,self.pages, ))

# 		# Запуск потоков на получение данных
# 		WildBerries.start()
# 		# Ozon.start()
# 		# Citilink.start()
# 				#Цикл block in container
# 				#новую позицию сразу вносит с проверкой в SQLITE

# 				#Функция добавления в общий словарь выпарсенных данных в result
# 			# Закрывается поток
# 		#Закрывается поток

# def Persona(a = 0):
# 	searchn = FormingDataForRequest('Крем')
# 	searchn.run()

# Persona = Thread(target=Persona, args=(1, ))
# # Persona.start()





# temp_time_start = datetime.datetime.now()
# chromedriver_path = 'C:\swdriver\chromedriver.exe'
# options = webdriver.ChromeOptions()
# options.add_argument('headless')

# linkJ = ['https://www.wildberries.ru/catalog/17267659/detail.aspx?targetUrl=MI',
# 		 'https://www.ozon.ru/',
# 		 'https://aliexpress.ru/?spm=a2g0o.detail.1000002.1.4e6e4885xpjQt6',
# 		 'https://www.citilink.ru/catalog/televizory--televizory-smart-tv/']

# driver = webdriver.Chrome(executable_path = chromedriver_path,chrome_options=options)
# driver.get(linkJ[0])
# massive = []
# # Access requests via the `requests` attribute
# print('start')
# for request in driver.requests:
# 	if request.response:
# 		# if request.url.find('https://wbxcatalog-ru.wildberries.ru/') != -1:
# 		# print(request.response.body.decode())
# 		# print(request.response.status_code)
# 		# print(request.response.headers['Content-Type'])
# 		# massive.append(request.response.body)
# 		massive.append(request.url)

# with open('out.txt', 'w', encoding='utf-8') as fp:# собираем то, что в файл попадет(data), +имя фйала(filename)+ расширение, открываем неа запись(w)
# 	print(massive, file=fp, sep="\n")# запись в файл с переводом строки
# 	fp.close()# закрытие файла

# temp_time_end = datetime.datetime.now()
# print(temp_time_end-temp_time_start)

#	th_jump = Thread(target=Jump_paral, args=(1, ))
#	th_jump.start()

#Сервер который ждет когда ему отправят вебхук, отдельный поток
#Разобрать возможные запросы и возвращаемые данные, подумать над тем как передать большие объемы данных
#Сервер после получения запроса на сервер, проводит обновление бд выше
#Работает сокетами, на каждого юзера свой поток, есть несколько типов запроса, поиск, информация о товаре
#Авторизация начинает поток пользователя, живой обмен сокетами с сервером

#Сортировка во время отправки данных по запросу

#Авторизация это просто запрос на функцию создания потока для человека на ПК

#Отслеживаемое
#Работа с ВК ботом
#Интерфейс вк это отдельный сервер, который работает с БД пользователей и их отслеживаемого, который на фоне работает в потоке и ждет изменения статуса сообщения

#Отслеживаемое отдельный сервер который взаимодействует с остальными, он в отдельном потоке отслеживает отслеживаемое на фоне, и если цена меняется то кидает запрос на сокет вк и клиента.
# Отслеживание идет втупую парся страницу 
# Защита бота отслеживания
# Есть БД товаров которые нужно проверить
# Для огромного количества нужна защита 
# Запускается поочередно на каждого юзера поток, в котором его отслеживаемое в рандомное время в течении 10 мин обновляется
# Алгоритм которые будет в прогрессии просчитывать нормы
# Подготовить разные хеадеры хз зачем


#Добавление товара отдельная функция

# Принимает *




	# def parse_block(self,block):
	# 	global i
	# 	# print(block)
	# 	# logger.info(block)
	# 	# logger.info('=' * 100)
	# 	url_block = block.select_one('a.o1se_.RAorI')
	# 	if not url_block:
	# 		logger.error('no url_block')
	# 		return

	# 	url = url_block.get('href')
	# 	if not url:
	# 		logger.error('no href')
	# 		return
		
	# 	name_block = block.select_one('div.ICmra')
	# 	if not name_block:
	# 		logger.error('no name_block on {url}')
	# 		return
	# 	brand_name = name_block.select_one('div._2CcHd')
	# 	if not brand_name:
	# 		logger.error('no brand_name on {url}')
	# 		return
	# 	brand_type = name_block.select_one('div._1pNLw')
	# 	if not brand_type:
	# 		logger.error('no brand_type on {url}')
	# 		return
	# 	brand_name = brand_name.text
	# 	brand_type = brand_type.text
	# 	brand_name = brand_name.replace('/','').strip()
#Кеширование на клиенте

# Таблица хранит поядок, id уник ссылка, + платформа
# в столбик заполняется заранее известные характеристики, но что делатьс датами?
# Сделать отдельный столбец, в него дату добавлять к предыдущей, в столбик складируются даты.
# Дополнить двумя магазами, вынести общее, заобщить функции, добавить функции нахождения точных данных по переменным, там же загрузка их в ячейки склайт

# Добавить обновлялку которая будет работать на фоне в неск потоках циклом, беск цикл который ходит по ячейкам, и как только находится подходящую закидывает обновление, сделать экономный алгоритм по таймеру и сортировке на фоне

# Настроить БД авторизации, создать и сделать форматы с запросами
# Настроить на каждого пользователя отслеживаемое, в одну колонку, проходится по каждому отслеживаемому и обновляет, если есть резльутат то сообщает
# Сообщает в функцию общения, отправки на аккаунт привязанный,
# Добавить функцию привязки и проверки, 

# Настроить общение клиент-сервер (большие данные)

# Примерный сервер готов, начинаю писать клиент

# Затем делаю плюшку в виде общения вк, улучшаю интерфейс, 
#Пытаюсь заменить парсер чтоб улучшить ситуацию
# Провожу выдержки и тесты, нахожу порог боли* и сохраняю
# Пишу курсовую про, сервер, сокетное общение или фласк, устрйостве, потоках, способах парса, базе данных, системе безопасности, клиент на чем, какие есть возможности, про вк бота, с помощью чего и как, что может.
