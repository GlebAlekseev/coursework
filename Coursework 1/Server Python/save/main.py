import requests
import bs4
from threading import Thread, Lock
import datetime
import logging
import re
import os
import json
import platform
from selenium import webdriver
from seleniumwire import webdriver  
import json
from fake_headers import Headers
import sqlite3
#Линки с магазинами на поиск
import urllib3
import certifi
import urllib.parse
import copy
import redis
# r = redis.Redis(db=0)
# r.hset("obj",{"id": "1", "subjectId": "010", "name": "Nassau"})
# print(r.keys())
# get("Bahamas").decode("utf-8")
import random
import json
import hashlib
from nickname_generator import generate
random.seed(444)
hats = {}
import datetime
import time

Links_storage = {'Wildberries': ['https://wbxsearch.wildberries.ru/exactmatch/v2/common?query=REQUEST&_app-type=sitemobile',
								 'https://wbxcatalog-ru.wildberries.ru/BUCKET/catalog?PRESET&appType=2&spp=0&regions=68,75,69,40,48,33,70,64,1,4,38,30,71,22,31,66&stores=119261,122252,122256,117673,122258,122259,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124093,124094,124095,124096,124097,124098,124099,124100,124101,120762,119400,116433,507,3158,120602,6158,117501,121709,2737,117986,1699,1733,686,117413,119070,118106,119781&pricemarginCoeff=1&pricemarginMin=0&pricemarginMax=0&reg=0&emp=0&lang=ru&locale=ru&version=3&curr=rub&page=PAGE',
								 'https://wbxcatalog-ru.wildberries.ru/SHARD/catalog?SUBJECT&search=NAME&page=PAGE&appType=2&spp=0&regions=68,75,69,40,48,33,70,64,1,4,38,30,71,22,31,66&stores=119261,122252,122256,117673,122258,122259,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124093,124094,124095,124096,124097,124098,124099,124100,124101,120762,119400,116433,507,3158,120602,6158,117501,121709,2737,117986,1699,1733,686,117413,119070,118106,119781&pricemarginCoeff=1&pricemarginMin=0&pricemarginMax=0&reg=0&emp=0&lang=ru&locale=ru&version=3&curr=rub'],
				 'my-shop':		['http://my-shop.ru/cgi-bin/shop2.pl?q=search&sort=z&page=PAGE&f14_6=REQUEST',
					  	    	 'https://my-shop.ru/cgi-bin/shop2.pl?q=product&id=3143442'],
				 'eldorado':	['https://www.eldorado.ru/sem/v3/a408/products?rootRestrictedCategoryId=0&query=REQUEST&orderField=popular&limit=50&offset=PAGE&regionId=11324',
								 'https://api.retailrocket.net/api/1.0/partner/5ba1feda97a5252320437f20/items/?itemsIds=71112985&stock=&format=json'],
					  	    	 }
					  	    	 # Wildberries 100
					  	    	 # my-shop 36
					  	    	 # eldorado 50


start =datetime.datetime.now()

New_updated_data = []

class Create_a_database_based_on_the_search_query:
	def __init__(self,request_name,links_storage = Links_storage):
		self.redisDB = redis.Redis(db=1)
		self.request_name = request_name
		if len(request_name) == 0:
			return
		self.links_storage = links_storage
		self.session = requests.Session()
		headers= Headers(
        browser="chrome",
        os="win", 
        headers=True 
    	)
		self.session.headers = headers.generate()
		self.pages = 1
		self.result = []
		self.products = {}




	def WildBerries_add(self,a):
		newurl = self.links_storage['Wildberries'][0].replace("REQUEST",str(self.request_name))
		res = self.session.get(url=newurl)
		res.raise_for_status()
		data_find_filters_decode = []
		data_find_filters_decode = json.loads(res.text)
		if len(data_find_filters_decode) == 0: # Пустой ответ от Wildberries
			print("Ничего не найдено Wildberries")
		else:
			i=0
			page_threads = []
			def PageInWild_d(a):
				# print("page",a)
				# print('Страница ', i)
				if data_find_filters_decode["query"].find("subject=") != -1:
					newurl = self.links_storage['Wildberries'][2].replace("PAGE",str(i+1)).replace("SHARD",str(data_find_filters_decode["shardKey"])).replace("SUBJECT",str(data_find_filters_decode["query"])).replace("NAME",str(data_find_filters_decode["name"]))
				elif data_find_filters_decode["query"].find("preset=") != -1:
					newurl = self.links_storage['Wildberries'][1].replace("PAGE",str(i+1)).replace("BUCKET",str(data_find_filters_decode["shardKey"])).replace("PRESET",str(data_find_filters_decode["query"]))
				else:
					return # Неудачный запрос
				res = self.session.get(url=newurl)
				
				# try:
				# 	res.raise_for_status()
				# except requests.exceptions.HTTPError:
				# 	self.check_full = False
				# 	return
				# print(res.raise_for_status())
				# print("page",a)
				data_decode = []
				try:
					data_decode = json.loads(res.text)
				except json.decoder.JSONDecodeError:
					return
				
				last_history = str(time.time())
				if len(data_decode['data']['products']) == 0:
					# print("-page",a)
					pass
				u = 0
				# delete_tr = 1# delete
				for item in data_decode['data']['products']:
					u+=1
					if self.st == -2:
						New_updated_data.append({'id':'W_iD'+str(item["id"]),'price':item["priceU"],'last_history':last_history})
						continue
					# if delete_tr:
					# 	print(item)
					smart_id = str(item["id"])[0:-4] +4*"0"
					# print("smart= ",smart_id)
					# smart_id = str(item["id"])[0:4] +(len(str(item["id"]))-4)*"0"
					# print(item["id"])
					# print(smart_id, "here")

					url_profile = "https://www.wildberries.ru/catalog/"+str(item["id"]) +"/detail.aspx?"
					url_brand_logo = "https://images.wbstatic.net/brands/small/new/" + str(item["siteBrandId"])+ ".jpg"
					url_img =  "https://images.wbstatic.net/c516x688/new/"+str(smart_id)+"/"+str(item["id"])+"-1.jpg"
					# 	delete_tr = 0

					# print(url_profile)
					# print(url_brand_logo)
					# print(url_img)
					self.products.update({'W_iD'+str(item["id"]):	{'id':item["id"],'name':item["name"],'brandId':item["brandId"],'subjectId':item["subjectId"],
																			 'brand':item["brand"],'sale':item["sale"],'price':str(int(item["priceU"])/100),'salePriceU':item["salePriceU"],
																			 'pics':item["pics"],'rating':item["rating"],'feedbacks':item["feedbacks"],
																			 'last_history':last_history,
																			 'url_profile':url_profile, 'url_brand_logo':url_brand_logo,
																			 'url_img':url_img
																		 					}})
				# print("Wildberries ",u," позиций собрано.")
			
			# print("1")
			# self.check_full = False
			# if a==-1:
			# 	self.check_full = True
			if a==-1:
				# print()
				newurl = 'https://www.wildberries.ru/catalog/0/search.aspx?&search=REQUEST'.replace("REQUEST",str(self.request_name))
				res = self.session.get(url=newurl)
				soup = bs4.BeautifulSoup(res.text, 'lxml')
				container = soup.select('span.goods-count.j-goods-count')
				max_items = ''.join([i for i in str(container) if i.isdigit()])
				a=int(max_items)/100 *0.8
				# Max_pages = str(container[0]).split('найдено')[1].split('товаров')[0].strip()

			else:
				a=a*0.92
				#Получить макс число страниц
			# print(2)
			while i<a:
				# print(i)
				# print("F")
				page_threads.append(Thread(target=PageInWild_d, args=(i, )))
				page_threads[i].start()
				i+=1
			j=0
			for page_th in page_threads:
				page_th.join()
				# print(j,end = ' ')
				j+=1
		# print("end-pages-cikle")


	def Eldorado_add(self,a): # Добавить доп ячейки и добав в БД

			urlHowmuchPages = 'https://www.eldorado.ru/search/catalog.php?q=' + self.request_name
			tmpPgs= self.session.get(url=urlHowmuchPages)
			tmpPgs.raise_for_status()
			soup = bs4.BeautifulSoup(tmpPgs.text, 'lxml')
			container = soup.select('p.Wi') # не стабильно
			# print(container)
			Max_pages =''.join([i for i in str(container)[str(container).find('найден'):str(container).find('товар')] if i.isdigit()])		
			print(container,"container Max_Pages")
			print(Max_pages,"Max_Pages")
			if not Max_pages.isdigit() :
				print("Ничего не найдено Eldorado")
				return
			# Max_pages = 	''.join([i for i in str(str(str(container).split('товаров')[0]).split('найдено')[1]) if i.isdigit()])

			# print(Max_pages)
			newurl = self.links_storage['eldorado'][0].replace("REQUEST",str(self.request_name))
			i=0
			page_threads = []
			def PageInEld_d(a):
				# print(i)
				newurl_In = newurl.replace("PAGE",str(i*50))
				# print(newurl_In)
				res = self.session.get(url=newurl_In)
				res.raise_for_status()
				data_find_filters_decode = []
				data_find_filters_decode = json.loads(res.text)
				last_history = str(time.time())
				# print('Страница ', i)
				if len(data_find_filters_decode['data']) == 0:
					# print("page ",a)
					pass
				u=0
				# delete_tr = 1
				for item in data_find_filters_decode['data']:
					u+=1
					if self.st == -2:
						New_updated_data.append({'id':'E_iD'+str(item["id"]),'price':item["price"],'last_history':last_history})
						continue
					
					# if delete_tr:
					# 	print(item)
					# 	delete_tr = 0
					url_profile = "https://www.eldorado.ru/cat/detail/"+str(item["code"])
					try:
						url_img = "https://static.eldorado.ru"+str(item["images"][0]["url"])
						# print("yes")
					except IndexError:
						url_img=0
						# print("no")

					
					# print(url_profile )
					# print(url_img )
					self.products.update({'E_iD'+str(item["id"]):	{'id':item["id"],'name':item["name"],'brand':item["brandName"],'productIdd':item["productId"],
																	 'shortName':item["shortName"],'oldPrice':item["oldPrice"],'price':item["price"],'rating':item["rating"],
																			 'last_history':last_history,'feedbacks':item['numOfComment'],
																			 'url_profile':url_profile,'url_img':url_img
																			 					}})
				# print("Eldorado ",u," позиций собрано.")

					# print(item['id'],item['name'],item['shortName'],item['productId'],item['brandName'],item['price'],item['oldPrice'],item['rating'])
			# print(int(Max_pages)/50)

			# print(a)
			if a == -1 or a>int(Max_pages):

				a = int(Max_pages)/50 + 1

			print(a)
			while i<a:
				# print(i)
				page_threads.append(Thread(target=PageInEld_d, args=(i, )))
				page_threads[i].start()
				i+=1
			j=0
			for page_th in page_threads:
				page_th.join()
				# print(j,end = ' ')
				j+=1



				i+=1



	def myShop_add(self,a): # Добавить доп ячейки и добав в БД
		i=0
		newurl = self.links_storage['my-shop'][0].replace("REQUEST",urllib.parse.quote(str(self.request_name)))
		http = urllib3.PoolManager(ca_certs=certifi.where())
		payload = {'f14_6': self.request_name}
		encoded_data = json.dumps(payload).encode('utf-8')
		bodyM = urllib.parse.quote(str(self.request_name))
		page_threads = []
		def PageInMshop_d(a):
			# print("page",a)
			newurl_In = newurl.replace("PAGE",str(i+1))
			resp = http.request(
				'POST',
				newurl_In,
				body=encoded_data,
				headers={'Content-Type': 'application/json'})
			data = json.loads(resp.data.decode('utf-8'))
			try:
				if data['products'] is None:
					pass
			except KeyError:
				# print("-page ", a)
				return

			last_history = str(time.time())
			u=0
			# delete_tr=1
			for item in data['products']:
				u+=1
				# print(item['product_id'],item['cost'],item['title'],item['ga_item']['id'],item['ga_item']['brand'])
				if self.st == -2:
					New_updated_data.append({'id':'M_iD'+str(item['ga_item']['id']),'price':item["cost"],'last_history':last_history})
					continue
				# if delete_tr:
				# 		print(item)
				# 		delete_tr = 0
				url_profile = "https://my-shop.ru/shop/product/"+str(item["product_id"])+".html"
				url_img = "http://" + str(item["image"]["href"][2:])
				# print(url_profile)
				# print(url_img)
				self.products.update({'M_iD'+str(item['ga_item']['id']):	{'id':item['ga_item']['id'],'name':item['title'],'brand':item['ga_item']['brand'],'productIdd':item['product_id'],
																	 'price':item['cost'],
																			 'last_history':last_history,
																	 'url_profile':url_profile,'url_img':url_img
																			 					}})
			# print("myShop ",u," позиций собрано.")
		
		newurl_InH = newurl.replace("PAGE",str(1))
		resp = http.request(
				'POST',
				newurl_InH,
				body=encoded_data,
				headers={'Content-Type': 'application/json'})
		print("start",resp.data.decode('utf-8'),"end")
		data = json.loads(resp.data.decode('utf-8'))
		# print(a)
		# print(data['meta']['total']/40)
		if int(data['meta']['total']) == 0:
			print("Ничего не найдено myShop")
			return
		if int(data['meta']['total'])/40 < a or a==-1:
			a = int(data['meta']['total'])/40

		# print(a)
		while i<a:
			# print(i)
			page_threads.append(Thread(target=PageInMshop_d, args=(i, )))
			page_threads[i].start()
			i+=1
		j=0
		for page_th in page_threads:
			page_th.join()
			# print(j,end = ' ')
			j+=1









	def search_start(self,pages=10,Wild=True,ELD=False,MShop=False): # если -1 pages то парсит полностью
		self.st = 0
		if pages == -2:
			self.st = pages
			pages = -1
		# Получение активных запросов
		requests_names = self.redisDB.hgetall('requests_names')
		resR = []
		for key in requests_names:
			tmp = requests_names[key].decode('UTF-8')
			resR.append(key.decode('unicode_escape'))
			# print(resR[0].decode('unicode_escape')) # Список хороших запросов.
		#Проврека на повторный запрос
		status_repeat = False
		for req_name in resR:
			if '"'+self.request_name+'"' == req_name:
				status_repeat = True
		if status_repeat and self.st != -2:
			# print("Повторный запрос")
			pass
		else:
			# print("NEW")
			#ПАРСИНГ
			if Wild:
				WildBerries = Thread(target=self.WildBerries_add, args=(pages, ))
				WildBerries.start()
			if ELD:
				Eldorado = Thread(target=self.Eldorado_add, args=(pages, ))
				Eldorado.start()
			if MShop:
				myShop = Thread(target=self.myShop_add, args=(pages, ))
				myShop.start()

			if Wild:
				WildBerries.join()
			if ELD:
				Eldorado.join()
			if MShop:
				myShop.join()
			
			
			# 

			if self.st == -2:
				# Обновление времени на запросе в общаке
				self.redisDB.close()
				return

			#ВНОС В БД products и requests_names
			with self.redisDB.pipeline() as pipe:
				for h_id, hat in self.products.items():
					# print(json.dumps(h_id))
					pipe.hset("products",json.dumps(h_id),json.dumps(hat))
					# print(json.dumps(hat))
					# pipe.expire("products", datetime.timedelta(seconds=1))
				# print(h_id,"h+id")
				pipe.hset("requests_names",json.dumps(str(self.request_name)),json.dumps(str(time.time())))
				# pipe.expire("products", datetime.timedelta(minutes=30))
				pipe.hset("requests_save_names",json.dumps(str(self.request_name)),json.dumps(str(time.time())))
				pipe.execute()
		
			

			






		#Получение данных на отправку

		result = self.redisDB.hgetall('products')
		resW = []
		for key in result:
			tmp = result[key].decode('UTF-8')
			resW.append(key.decode('UTF-8'))

			# if json.loads(tmp)['name'].find("Fu") != 1:
			# print(key.decode('UTF-8'), '->', json.loads(tmp)['name'], '->',json.loads(tmp)['brand'],'->',json.loads(tmp)['price'])
		print()
		print("Собрано",len(resW),"единиц товара. По запросу",self.request_name)
		# 		resW.append(json.loads(tmp)['name'])
		# resW.sort()
		# print(resW)


		# print(self.products)
		# self.connect.commit()
		# print("commit")
		# self.connect.close()
		# self.redisDB.bgsave()
		self.redisDB.close()

		# print("close")



class collectors:
	def __init__(self):
		self.redisDB = redis.Redis(db=1)

	# ЗАПУСК Сборщик мусора, запросов  КАЖДЫЕ 10 минут
	def bad_request_collector(self,a):
		while True:
			result = self.redisDB.hgetall('requests_names')
			for key in result:
				tmp = result[key].decode('UTF-8')
				if float(tmp.strip('"'))+60*10 <time.time():
					self.redisDB.hdel("requests_names",key)
					print("#delete ",key.decode('unicode_escape'))
			time.sleep(60*10) # Каждые 10 мин включается
	# ЗАПУСК Сборщик мусора, Товаров last_history # Каждые 10 мин включается
	def bad_position_collector(self,a):
		while True:
			result = self.redisDB.hgetall('products')
			for key in result:
				# print("Цикл")
				# print(json.loads(result[key].decode('unicode_escape'))['last_history'])
				# print(key)
				# print(str(json.loads(result[key].decode('UTF-8'))['last_history']))
				if float(str(json.loads(result[key].decode('UTF-8'))['last_history']))+60*10 <time.time():
					# Переход в построение истории
					New_updated_data.append({'id':key.decode('UTF-8'),'price':json.loads(result[key].decode('UTF-8'))['price'],'last_history':json.loads(result[key].decode('UTF-8'))['last_history']})# Сейвит ИД, цену, ласт_хистори (потом рейтинг)
					temp = key
					self.redisDB.hdel("products",key)

			print(" осталось ",len(self.redisDB.hgetall('products')))
			# print(self.redisDB.hgetall('products'))
			time.sleep(60*10)

	def run(self):
		Thread_bad_request_collector = Thread(target=self.bad_request_collector, args=(1, ))
		Thread_bad_request_collector.start()

		Thread_bad_position_collector = Thread(target=self.bad_position_collector, args=(1, ))
		Thread_bad_position_collector.start()




class Updating_Master_data:
	def processing_all_requests(self,a):



		while True:
			self.redisDB = redis.Redis(db=1)
			result = self.redisDB.hgetall('requests_save_names')
			resW = []
			connect = sqlite3.connect("data.db") # или :memory: чтобы сохранить в RAM
			connect.isolation_level= 'DEFERRED'
							# connect.execute('''PRAGMA synchronous = OFF''')
							# connect.execute('''PRAGMA journal_mode = OFF''')
			cursor = connect.cursor()
			try:
				cursor.execute("""CREATE TABLE items_history
											(id text, price text, last_history text )
											""")
			except sqlite3.OperationalError:
				print("БД уже создана")
			else:
				print("Создание БД")

			# print(result)
			for key in result:
				tmp = result[key].decode('UTF-8')
				if float(tmp.strip('"'))+60*60*12/(60*12) < time.time(): # если данные не обновлялись 12 часов
					# print(key.decode('unicode_escape').strip('"'))

					# Запуск обновления
					# Обновление времени обновления по запросу
					Create_a_database_based_on_the_search_query(key.decode('unicode_escape').strip('"')).search_start(-2) #  -2 значит полностью, внутри функции добавляет в массив
					if len(New_updated_data) > 10000: # превышает 10к
						# print("IN DATA BASE")

						
						for element in New_updated_data:
							# print(element)
							
							info = cursor.execute('SELECT * FROM items_history WHERE id=?', (element["id"], ))
							if info.fetchone() is None:  # Записи нет
								# print("Нету")
								data = (element["id"], element['price'],element['last_history']) 
								# print(data)
								cursor.execute("INSERT INTO items_history VALUES (?,?,?)", data)
							else:# Запись есть
								# print("Есть")

								#Делаем когда есть человек в бд
								# info = cursor.execute('SELECT * FROM items_history WHERE id=?', (element["id"], ))
								records = cursor.fetchall()
								for record in records:
									print("ex",record[0])
									print("ex",record[1])
									print("ex",record[2])
									print("el",element['last_history'])
									print("el",element['price'])

									history = str(record[2]) + '\n' + element['last_history']
									price = str(record[1]) + '\n' + str(element['price'])
									# print(record)
									cursor.execute('UPDATE items_history SET  price = ?,last_history = ? WHERE id = ?',(price,history,record[0], ))


								# history = str(records[0]).replace('(','').replace(')','').split(',') # Добавить историю цен
								# print("history1",history)
								# history = history[2].replace("'",'').strip() + '\n' + element['last_history']
								# print("history2",history)

								# price = str(records[0]).replace('(','').replace(')','').split(',') # Добавить историю цен
								# price = str(price[1]).replace("'",'').strip() + '\n' + str(element['price'])

			connect.commit()
			connect.close()		
						
						# Формирование истории цен
						# Узнает, есть ли такая же запись, если есть добавляет иначе вставляет
						# внос в sqlite
			# 	print(result)
			# 	with self.redisDB.pipeline() as pipe:
			# 		for h_id, hat in result.items():
			# 			pipe.hset("requests_save_names",json.dumps(str(key.decode('unicode_escape').strip('"')),json.dumps(str(time.time()))))
			# 		pipe.execute()
			# self.redisDB.close()




					# Проверка если количество позиций в глоб массиве превышает 100к то вносит в sqlite
					# обновляет дату ласт обновления реквеста

					# Внос в sqlite отдельная функция


				# print(tmp.strip('"'))
				# print(key.decode('unicode_escape').strip('"'))
			
			print("END update")
			time.sleep(60*60*6/(6*30)) # Каждые 12 часов

	def run(self):
		Thread_updating_information = Thread(target=self.processing_all_requests, args=(1, ))
		Thread_updating_information.start()
		# Цикл по всем запросам и хгеталл
		# Настроить получение данных с новым параметром, для парса фула без доабвления в бд, только для обновления бд ид цена дата (рейтинги, комменты и другое)
		# Класс по настройке добавит в глоб
		#Тут ожидание, один поток общий, ожидание всех зарпосов из бд, между циклами каждого запроса, проверка на кол-во единиц, при превышении 100к добавление в sqlite/


# class обновляет отдельные элементы из sqlite профиля


		



# Добавить класс для обновления отслеживаемого (единичное обновление)

# Добавить класс на уведомление

# Добавить профили, регистрацию





# Организовать взаимодействие клиент-сервер.


# Дополнить проверками на ошибки. + тест
# Добавить еще парочку магазинов - не более 5

# New_updated_data








# Updating_Master_data().run()
# # Запуск сборщиков
# collectors().run()



import random
# Сервер для общения с клиентом
import hashlib
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"




		# Авторизация
# Логирование
# Регистрация
# Смена пароля

# Во всех запросах есть Hash вместе с логином сверяет в бд и при наличии продолжает иначе возвращает вы не авторизованы


# Кеш хранить в редисе
@app.route("/checkauth", methods=['POST'])
def checkauth():
	connect = sqlite3.connect("data.db") 
	connect.isolation_level= 'DEFERRED'
	cursor = connect.cursor()
	try:
		cursor.execute("""CREATE TABLE users
			(id INTEGER PRIMARY KEY, login text, password text,hash text,key text,last_session_update text)
			""") # Ячейки в таблице (добавить по ходу)
	except sqlite3.OperationalError:
		print("БД уже создана")
		pass
	else:
		print("Создание БД")
		pass

	login = json.loads(request.data.decode('UTF-8'))['login']
	hash_ = json.loads(request.data.decode('UTF-8'))['hash']
	hash_time = json.loads(request.data.decode('UTF-8'))['hash_time']
	info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))

	if info.fetchone() is None:
		connect.close()	
		return "104" # Неверный сейв
	else:
		info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))
		for i in info:
			# print(str(i).replace('(','').replace(')','').split(','))
			hash_bd = str(i).replace('(','').replace(')','').split(',')[3]
			hash_time_bd = str(i).replace('(','').replace(')','').split(',')[5]
			break

		hash_bd = hash_bd.replace("'",'').strip()
		hash_time_bd = hash_time_bd.replace("'",'').strip()


		if float(time.time()) -60*60*24*30 < float(hash_time_bd):

			if hash_ == hash_bd:
				connect.close()	
				return "Go"
			else:
				connect.close()	
				return "106" # Неверный хеш
		else:
			connect.close()	
			return "105" # Устаревший в бд сейв







@app.route("/login", methods=['POST'])
def login():
	connect = sqlite3.connect("data.db") 
	connect.isolation_level= 'DEFERRED'
	cursor = connect.cursor()
	try:
		cursor.execute("""CREATE TABLE users
			(id INTEGER PRIMARY KEY, login text, password text,hash text,key text,last_session_update text)
			""") # Ячейки в таблице (добавить по ходу)
	except sqlite3.OperationalError:
		print("БД уже создана")
		pass
	else:
		print("Создание БД")
		pass

	login = json.loads(request.data.decode('UTF-8'))['login']
	password = json.loads(request.data.decode('UTF-8'))['password']

	info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))

	if info.fetchone() is None:
		connect.close()	
		return "102" # Неверные данные
	else:
		info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))
		for i in info:
			print(str(i).replace('(','').replace(')','').split(','))
			password_bd = str(i).replace('(','').replace(')','').split(',')[2]
			key_bd = str(i).replace('(','').replace(')','').split(',')[4]
			break
		password_bd = password_bd.replace("'",'').strip()
		key_bd = key_bd.replace("'",'').strip()

		password_curr = hashlib.md5(str(str(password) +str(key_bd) ).encode()).hexdigest()
		print(password_bd, "bd")
		print(password_curr, "curr")
		if password_curr == password_bd:
			#Новый хеш
			hash_ = hashlib.md5((str(password_bd)+str(key_bd)+str(time.time())).encode()).hexdigest()# Ключ к сессии длительностью 1 день
			last_session_update = time.time();
			
			cursor.execute('UPDATE users SET hash = ?,last_session_update = ? WHERE login = ?',(hash_,last_session_update,login, ))
			connect.commit()
			connect.close()
			return str(hash_)
		connect.close()
		return "103"






@app.route("/register", methods=['POST'])
def register():
	connect = sqlite3.connect("data.db") 
	connect.isolation_level= 'DEFERRED'
	cursor = connect.cursor()
	try:
		cursor.execute("""CREATE TABLE users
			(id INTEGER PRIMARY KEY, login text, password text,hash text,key text,last_session_update text)
			""") # Ячейки в таблице (добавить по ходу)
	except sqlite3.OperationalError:
		print("БД уже создана")
		pass
	else:
		print("Создание БД")
		pass

	login = json.loads(request.data.decode('UTF-8'))['login']
	password = json.loads(request.data.decode('UTF-8'))['password']

	info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))

	if info.fetchone() is None:
		# Добавить рандом в key
		key = hashlib.md5(str(login).encode()).hexdigest()
		password = hashlib.md5(str(str(password) +str(key) ).encode()).hexdigest()

		hash_ = hashlib.md5((str(password)+str(key)+str(time.time())).encode()).hexdigest()# Ключ к сессии длительностью 1 день
		last_session_update = time.time();
		data = (str(login), str(password),str(hash_),str(key),str(last_session_update)) 
		cursor.execute("INSERT INTO users  (login,password,hash,key,last_session_update)VALUES (?,?,?,?,?)", data)
		connect.commit()
		connect.close()
		return str(hash_)
	else:
		connect.close()
		return "101" # Ошибка: Логин занят
	







@app.route("/changepw", methods=['POST'])
def changePW():
	connect = sqlite3.connect("data.db") 
	connect.isolation_level= 'DEFERRED'
	cursor = connect.cursor()
	try:
		cursor.execute("""CREATE TABLE users
			(id INTEGER PRIMARY KEY, login text, password text,hash text,key text,last_session_update text)
			""") # Ячейки в таблице (добавить по ходу)
	except sqlite3.OperationalError:
		print("БД уже создана")
		pass
	else:
		print("Создание БД")
		pass

	login = json.loads(request.data.decode('UTF-8'))['login']
	curr_password = json.loads(request.data.decode('UTF-8'))['curr_password']
	new_password = json.loads(request.data.decode('UTF-8'))['new_password']

	info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))

	for i in info:
		print(str(i).replace('(','').replace(')','').split(','))
		password_bd = str(i).replace('(','').replace(')','').split(',')[2]
		key_bd = str(i).replace('(','').replace(')','').split(',')[4]
		break
		
	password_bd = password_bd.replace("'",'').strip()
	key_bd = key_bd.replace("'",'').strip()

	password_curr = hashlib.md5(str(str(curr_password) +str(key_bd) ).encode()).hexdigest()
	if password_curr == password_bd:
		
		# Смена пароля
		password = hashlib.md5(str(str(new_password) +str(key_bd) ).encode()).hexdigest()

		cursor.execute('UPDATE users SET password = ? WHERE login = ?',(str(password),str(login), ))
		connect.commit()
		connect.close()
		return "Go" # Смена прошла успешно

	else:
		# Текущий пароль неверно указан
		connect.close()
		return "108" # Текущий пароль неверно указан

@app.route("/search", methods=['POST'])
def search():
	request_text = json.loads(request.data.decode('UTF-8'))['request_text'] # Запрос

	SORTAZ = json.loads(request.data.decode('UTF-8'))['SORTAZ'] # Запрос
	SORT12 = json.loads(request.data.decode('UTF-8'))['SORT12'] # Запрос
	SHOPW = json.loads(request.data.decode('UTF-8'))['SHOPW'] # Запрос
	SHOPD = json.loads(request.data.decode('UTF-8'))['SHOPD'] # Запрос
	SHOPM = json.loads(request.data.decode('UTF-8'))['SHOPM'] # Запрос


	redisDB = redis.Redis(db=1)
	print("start", request_text)
	Create_a_database_based_on_the_search_query(request_text).search_start(10,SHOPW,SHOPD,SHOPM) # Обновляет позиции в Redis #


		# Получение активных запросов
	resR=[]

	request_receiveRaw = redisDB.hgetall('products')
	for key in request_receiveRaw:
		# request_receiveRaw[key]["Mid"]= key.decode('unicode_escape')

		tmp = request_receiveRaw[key].decode('UTF-8')
		temp = json.loads(tmp)
		temp["Mid"]= key.decode('unicode_escape').strip('"')

		resR.append(temp)

		
	resF = []
	for item in resR:
		if item["name"].find(request_text) != -1: # нашло
			# print(item["name"])
			resF.append(item)

	# ResF сортируется
	print(resF)
	def sort_list_data_name(data,ASC = True):
		n = len(data)
		if ASC:
			for i in range(n):
				for j in range(i + 1, n):
					if data[i]["name"] > data[j]["name"]:
						data[i]["name"], data[j]["name"] = data[j]["name"], data[i]["name"]
		else:
			for i in range(n):
				for j in range(i + 1, n):
					if data[i]["name"] < data[j]["name"]:
						data[i]["name"], data[j]["name"] = data[j]["name"], data[i]["name"]

	def sort_list_data_price(data,ASC = True):
		n = len(data)
		if ASC:
			for i in range(n):
				for j in range(i + 1, n):
					if float(data[i]["price"]) > float(data[j]["price"]):
						data[i]["price"], data[j]["price"] = data[j]["price"], data[i]["price"]
		else:
			for i in range(n):
				for j in range(i + 1, n):
					if float(data[i]["price"]) < float(data[j]["price"]):
						data[i]["price"], data[j]["price"] = data[j]["price"], data[i]["price"]
	sort_list_data_name(resF,SORTAZ) # ASC сортировка
	sort_list_data_price(resF,SORT12) # ASC сортировка
	for item in resF:
		print(item["url_img"])
	return json.dumps(resF)
	# key.decode('unicode_escape'),tmp
			# print(resR[0].decode('unicode_escape')) # Список хороших запросов.
		#Проврека на повторный запрос



	# Получить массив данных, оформить json и отправить на клиент 
	# Загрузить все страницы? или как?

	# Идея, добавить еще один пункт, и на каждые 10 страниц отправляется пак товаров
	#Сервер на фоне парсит все, делает быструю версию на первые 10 страниц и выдает ее,  остальное перепарсит и за вычетом 10 страниц отсортирует
	# Как идея...



# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)























@app.route("/add_to_tracked", methods=['POST'])
def add_to_tracked():
	login = json.loads(request.data.decode('UTF-8'))['login']
	Mid = json.loads(request.data.decode('UTF-8'))['Mid']

	try:
		status_ = json.loads(request.data.decode('UTF-8'))['status_']
	except KeyError:
		status_=False

	
	status = False

	print("login -",login,"Mid -",Mid)

	connect = sqlite3.connect("data.db") 
	connect.isolation_level= 'DEFERRED'
	cursor = connect.cursor()
	try:
		cursor.execute("""CREATE TABLE user_tracking
			(id INTEGER PRIMARY KEY, login text, Mid text,price_history text,time_history text,last_history text, setting_wait text, tracking text)
			""") # Ячейки в таблице (добавить по ходу)

		# login, Mid  # Хранит то что у каждого пользователя, хранит историю цен, историю врмен
		# В отслежке, циклом по Mid loginу, на каждый мид дает запрос отдельный, и полученные данные возвращает пользователю
		# Проверка обновления цены, бегает по таблице каждые настроенные тайминги и собирает ссылку через мид
		# делает запрос на получение данных, если данные изменились оно обновляет и добьавляет в таблицу
		# Для отпарвки уведомления, прямо в условии вставить функцию отправки инфы об этом.




		# Чекер будет собирать ближайшие тайминги, после обновления будет ставить следующий тайминг
	except sqlite3.OperationalError:
		print("БД уже создана")
		pass
	else:
		print("Создание БД")
		pass


	if status_:
		info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid=?' , (login,Mid ))
		if info.fetchone() is None:  # Добавление
			return "600"
		else:
			return "601"



	info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid=?' , (login,Mid ))



	if info.fetchone() is None:  # Добавление 
		data = (login,Mid,60*5,False) 
		cursor.execute("INSERT INTO user_tracking (login,Mid,setting_wait,tracking)VALUES (?,?,?,?)", data)
		connect.commit()
		print("600")
		return "600"
 
	else:# Уже добавлен
		if status:
			pass
			# Смена настроек
			connect.close()
			print("650")
			return "650"
		else:
			connect.close()
			print("601")
			return "601"
		
		# Возвращает 601 если ошибка повторного добавления ()
		# В данных передавать триггер, если тру то значит смена настроек, если фэлс по умолчанию то пропуск


	# connect = sqlite3.connect("data.db") 
	# connect.isolation_level= 'DEFERRED'
	# cursor = connect.cursor()
	# try:
	# 	cursor.execute("""CREATE TABLE users
	# 		(id INTEGER PRIMARY KEY, login text, password text,hash text,key text,last_session_update text)
	# 		""") # Ячейки в таблице (добавить по ходу)
	# except sqlite3.OperationalError:
	# 	print("БД уже создана")
	# 	pass
	# else:
	# 	print("Создание БД")
	# 	pass

	# login = json.loads(request.data.decode('UTF-8'))['login']
	# password = json.loads(request.data.decode('UTF-8'))['password']

	# info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))

	# if info.fetchone() is None:
	# 	# Добавить рандом в key
	# 	key = hashlib.md5(str(login).encode()).hexdigest()
	# 	password = hashlib.md5(str(str(password) +str(key) ).encode()).hexdigest()

	# 	hash_ = hashlib.md5((str(password)+str(key)+str(time.time())).encode()).hexdigest()# Ключ к сессии длительностью 1 день
	# 	last_session_update = time.time();
	# 	data = (str(login), str(password),str(hash_),str(key),str(last_session_update)) 
	# 	cursor.execute("INSERT INTO users  (login,password,hash,key,last_session_update)VALUES (?,?,?,?,?)", data)
	# 	connect.commit()
	# 	connect.close()
	# 	return str(hash_)
	# else:
	# 	connect.close()
	# 	return "101" # Ошибка: Логин занят
	

@app.route("/delete_to_tracked", methods=['POST'])
def delete_to_tracked():
	login = json.loads(request.data.decode('UTF-8'))['login']
	Mid = json.loads(request.data.decode('UTF-8'))['Mid']




	connect = sqlite3.connect("data.db") 
	connect.isolation_level= 'DEFERRED'
	cursor = connect.cursor()
	try:
		cursor.execute("""CREATE TABLE user_tracking
			(id INTEGER PRIMARY KEY, login text, Mid text,price_history text,time_history text,last_history text, setting_wait text, tracking text)
			""") # Ячейки в таблице (добавить по ходу)
	except sqlite3.OperationalError:
		print("БД уже создана")
		pass
	else:
		print("Создание БД")
		pass



	info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid=?' , (login,Mid ))


	if info.fetchone() is None:  # Добавление 
		connect.close()
		return "601"
 
	else:# Уже добавлен


		cursor.execute('DELETE FROM user_tracking WHERE login = ? AND Mid=?', (login,Mid ))
		connect.commit()


		connect.close()
		print("600")
		return "600"



















@app.route("/get_tracked", methods=['POST'])
def get_tracked():
	request_text = json.loads(request.data.decode('UTF-8'))['request_text'] # Запрос

	SORTAZ = json.loads(request.data.decode('UTF-8'))['SORTAZ'] # Запрос
	SORT12 = json.loads(request.data.decode('UTF-8'))['SORT12'] # Запрос
	SHOPW = json.loads(request.data.decode('UTF-8'))['SHOPW'] # Запрос
	SHOPD = json.loads(request.data.decode('UTF-8'))['SHOPD'] # Запрос
	SHOPM = json.loads(request.data.decode('UTF-8'))['SHOPM'] # Запрос

	login = json.loads(request.data.decode('UTF-8'))['login']



	connect = sqlite3.connect("data.db") 
	connect.isolation_level= 'DEFERRED'
	cursor = connect.cursor()


	try:
		cursor.execute("""CREATE TABLE user_tracking
			(id INTEGER PRIMARY KEY, login text, Mid text,price_history text,time_history text,last_history text, setting_wait text, tracking text)
			""") # Ячейки в таблице (добавить по ходу)
	except sqlite3.OperationalError:
		print("БД уже создана")
		pass
	else:
		print("Создание БД")
		pass

	resF= []

	info = cursor.execute('SELECT * FROM user_tracking WHERE login=?' , (login,))


	if info.fetchone() is None:  # Добавление 
		
		return "701" # В отслежке пусто

	else:# Уже добавлен
		info = cursor.execute('SELECT * FROM user_tracking WHERE login=?' , (login,))
		for item in info:
			# print(item[2])

			if SHOPW and str(item[2]).find("W_iD") !=-1:
				print("W")
				resF.append(item)
			if SHOPD and str(item[2]).find("E_iD") !=-1:
				print("E")
				resF.append(item)
			if SHOPM and str(item[2]).find("M_iD") !=-1:
				print("M")
				resF.append(item)



	fin_data_checked = []
	def get_data(resF):
		url_W = 'https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?spp=0&pricemarginCoeff=1.0&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=ru&lang=ru&curr=rub&nm=IDS;'
		url_E = 'https://api.retailrocket.net/api/1.0/partner/5ba1feda97a5252320437f20/items/?itemsIds=IDS&stock=&format=json'
		url_M = 'https://my-shop.ru/cgi-bin/shop2.pl?q=product&id=IDS'



		session = requests.Session()
		headers = Headers(
	        browser="chrome",
	        os="win", 
	        headers=True 
	    )
		session.headers = headers.generate()


		for item in resF:
			# print(item)
			if str(item[2]).find("W_iD") != -1:
				newurl = url_W.replace("IDS",str(item[2])[4:])
				res = session.get(url=newurl)
				res.raise_for_status()
				sd = json.loads(res.text)
				Mid = 'W_iD'+str(sd["data"]["products"][0]["id"])
				name = sd["data"]["products"][0]["name"]
				brand = sd["data"]["products"][0]["brand"]
				price = int(sd["data"]["products"][0]["priceU"])/100

				smart_id = str(sd["data"]["products"][0]["id"])[0:-4] +4*"0"

				url_img = "https://images.wbstatic.net/c516x688/new/"+str(smart_id)+"/"+str(sd["data"]["products"][0]["id"])+"-1.jpg"
				url_profile = "https://www.wildberries.ru/catalog/"+str(sd["data"]["products"][0]["id"]) +"/detail.aspx?"
				url_logo_brand = "https://images.wbstatic.net/brands/small/new/" + str(sd["data"]["products"][0]["siteBrandId"])+ ".jpg"

					

			if str(item[2]).find("E_iD") != -1:
				newurl = url_E.replace("IDS",str(item[2])[4:])
				res = session.get(url=newurl)
				res.raise_for_status()
				sd = json.loads(res.text)
				Mid = 'E_iD'+str(sd["data"]["products"][0]["id"])
				name = 0
				brand = 0
				price = 0
				url_img = 0
				url_profile = 0
				url_logo_brand = 0


			if str(item[2]).find("M_iD") != -1:
				newurl = url_M.replace("IDS",str(item[2])[4:])
				res = session.get(url=newurl)
				res.raise_for_status()
				sd = json.loads(res.text)
				Mid = 'M_iD'+'str(sd["data"]["products"][0]["id"])'
				name = 0
				brand = 0
				price = 0
				url_img = 0
				url_profile = 0
				url_logo_brand = 0



			if len(sd) == 0:
				continue



			# print(sd["data"]["products"][0])
			fin_data_checked.append((Mid,name,brand,price,url_img,url_profile,url_logo_brand))	
	get_data(resF)


	connect.close()
	redisDB = redis.Redis(db=1)
	print("start", request_text)
	# Create_a_database_based_on_the_search_query(request_text).search_start(10,SHOPW,SHOPD,SHOPM) # Обновляет позиции в Redis #

	def sort_list_data_name(data,ASC = True):
		n = len(data)
		if ASC:
			for i in range(n):
				for j in range(i + 1, n):
					if data[i]["name"] > data[j]["name"]:
						data[i]["name"], data[j]["name"] = data[j]["name"], data[i]["name"]
		else:
			for i in range(n):
				for j in range(i + 1, n):
					if data[i]["name"] < data[j]["name"]:
						data[i]["name"], data[j]["name"] = data[j]["name"], data[i]["name"]

	def sort_list_data_price(data,ASC = True):
		n = len(data)
		if ASC:
			for i in range(n):
				for j in range(i + 1, n):
					if float(data[i]["price"]) > float(data[j]["price"]):
						data[i]["price"], data[j]["price"] = data[j]["price"], data[i]["price"]
		else:
			for i in range(n):
				for j in range(i + 1, n):
					if float(data[i]["price"]) < float(data[j]["price"]):
						data[i]["price"], data[j]["price"] = data[j]["price"], data[i]["price"]

	# sort_list_data_name(fin_data_checked,SORTAZ) # ASC сортировка
	# sort_list_data_price(fin_data_checked,SORTpos12) # ASC сортировка
	# for item in resF:
	# 	print(item["url_img"])



	for item in fin_data_checked:
		print(item)
	return json.dumps(fin_data_checked )
	# key.decode('unicode_escape'),tmp
			# print(resR[0].decode('unicode_escape')) # Список хороших запросов.
		#Проврека на повторный запрос



	# Получить массив данных, оформить json и отправить на клиент 
	# Загрузить все страницы? или как?

	# Идея, добавить еще один пункт, и на каждые 10 страниц отправляется пак товаров
	#Сервер на фоне парсит все, делает быструю версию на первые 10 страниц и выдает ее,  остальное перепарсит и за вычетом 10 страниц отсортирует
	# Как идея...



# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)























@app.route("/get_history", methods=['POST'])
def get_history():
	Mid = json.loads(request.data.decode('UTF-8'))['Mid'] # Запрос
	# Получить данные из таблицы
	connect = sqlite3.connect("data.db") # или :memory: чтобы сохранить в RAM
	connect.isolation_level= 'DEFERRED'
						# connect.execute('''PRAGMA synchronous = OFF''')
						# connect.execute('''PRAGMA journal_mode = OFF''')
	cursor = connect.cursor()
	try:
		cursor.execute("""CREATE TABLE items_history
										(id text, price text, last_history text )
										""")
	except sqlite3.OperationalError:
		print("БД уже создана")
	else:
		print("Создание БД")
		connect.close()
		return "801" # Даже БД не создана значит возвращать нечего

	history_items = []
	info = cursor.execute('SELECT * FROM items_history WHERE id=?', (Mid, ))
	if info.fetchone() is None:  # Если нет истории у этого айтема
		connect.close()
		return "802"
	else:
		info = cursor.execute('SELECT * FROM items_history WHERE id=?', (Mid, ))

		for item in info:
			print(item[1])
			print(item[1].split("\n"))
			print(item[2].split("\n"))
			# for list_price in item[1].split("\n"):
			# 	print(list_price)
			# for list_time in item[2].split("\n"):
			# 	print(list_time)

			history_items.append((item[0],item[1],item[2]))	

		connect.close()
		return json.dumps(history_items)










if __name__ == '__main__':
	collectors().run() # Сборщик мусора в Redis товарных позициях
	Updating_Master_data().run()
	app.run(debug=True, port=5000,threaded=True)




# ТЕСТ ЗАПРОСЫ
# Create_a_database_based_on_the_search_query('мыло').search_start(-1) # PAGES
# Create_a_database_based_on_the_search_query('мясо').search_start(-1) # PAGES
# Create_a_database_based_on_the_search_query('гриль').search_start(-1) # PAGES
# Create_a_database_based_on_the_search_query('белый квадрат').search_start(-1) # PAGES
# for x in New_updated_data:
# 	print(x)
# Create_a_database_based_on_the_search_query('мыло').search_start(-1) # PAGES
# Create_a_database_based_on_the_search_query('мыло').search_start(30) # PAGES


# print('end')
print('Завершил сеанс за ', (datetime.datetime.now() - start))

