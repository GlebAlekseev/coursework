import requests
import bs4
from threading import Thread, Lock
import datetime
import logging

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



# connect = sqlite3.connect(":memory:")


# Подогнать бд
# lock = Lock()

class Create_a_database_based_on_the_search_query:
	def __init__(self,request_name,links_storage = Links_storage):
		self.redisDB = redis.Redis(db=1)
		self.request_name = request_name
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
			print("Ничего не найдено")
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
				res = self.session.get(url=newurl)
				# res.raise_for_status()
				data_decode = []
				data_decode = json.loads(res.text)
				last_history = str(datetime.datetime.now())
				if len(data_decode['data']['products']) == 0:
					# print("-page",a)
					pass
				for item in data_decode['data']['products']:
					self.products.update({'W_iD'+str(item["id"]):	{'id':item["id"],'name':item["name"],'brandId':item["brandId"],'subjectId':item["subjectId"],
																			 'brand':item["brand"],'sale':item["sale"],'price':item["priceU"],'salePriceU':item["salePriceU"],
																			 'pics':item["pics"],'rating':item["rating"],'feedbacks':item["feedbacks"],
																			 'last_history':last_history
																			 					}})
			while i<a*0.92:
				# print(i)
				page_threads.append(Thread(target=PageInWild_d, args=(i, )))
				page_threads[i].start()
				i+=1
			j=0
			for page_th in page_threads:
				page_th.join()
				# print(j,end = ' ')
				j+=1
		print("end-pages-cikle")


	def Eldorado_add(self,a): # Добавить доп ячейки и добав в БД

			urlHowmuchPages = 'https://www.eldorado.ru/search/catalog.php?q=' + self.request_name
			tmpPgs= self.session.get(url=urlHowmuchPages)
			tmpPgs.raise_for_status()
			soup = bs4.BeautifulSoup(tmpPgs.text, 'lxml')
			container = soup.select('p.squ9vk-0.jkgtrh')

# str(container[0]).split('найдено')[1].split('товаров')[0].strip()

# 		temp_time_end = datetime.datetime.now()
# 		# print(container)
			Max_pages = str(container[0]).split('найдено')[1].split('товаров')[0].strip()
			# print(Max_pages)
			newurl = self.links_storage['eldorado'][0].replace("REQUEST",str(self.request_name))
			i=0
			page_threads = []
			def PageInEld_d(a):
				newurl_In = newurl.replace("PAGE",str(i*50))
				# print(newurl_In)
				res = self.session.get(url=newurl_In)
				res.raise_for_status()
				data_find_filters_decode = []
				data_find_filters_decode = json.loads(res.text)
				# print('Страница ', i)
				if len(data_find_filters_decode['data']) == 0:
					# print("page ",a)
					pass
				for item in data_find_filters_decode['data']:
					self.products.update({'E_iD'+str(item["id"]):	{'id':item["id"],'name':item["name"],'brand':item["brandName"],'productIdd':item["productId"],
																	 'shortName':item["shortName"],'oldPrice':item["oldPrice"],'price':item["price"],'rating':item["rating"]
																			 					}})

					# print(item['id'],item['name'],item['shortName'],item['productId'],item['brandName'],item['price'],item['oldPrice'],item['rating'])
			while i<int(Max_pages)/50 + 1:
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


			for item in data['products']:
				# print(item['product_id'],item['cost'],item['title'],item['ga_item']['id'],item['ga_item']['brand'])
				self.products.update({'M_iD'+str(item['ga_item']['id']):	{'id':item['ga_item']['id'],'name':item['title'],'brand':item['ga_item']['brand'],'productIdd':item['product_id'],
																	 'price':item['cost']
																			 					}})
		
		newurl_InH = newurl.replace("PAGE",str(1))
		resp = http.request(
				'POST',
				newurl_InH,
				body=encoded_data,
				headers={'Content-Type': 'application/json'})
		data = json.loads(resp.data.decode('utf-8'))

		if int(data['meta']['total'])/40 < a :
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









	def search_start(self,pages=10): # Разбить на потоки, добавить или убрать алик, решить проблему с поштучной проверкой
		WildBerries = Thread(target=self.WildBerries_add, args=(pages, ))
		WildBerries.start()

		Eldorado = Thread(target=self.Eldorado_add, args=(pages, ))
		Eldorado.start()

		myShop = Thread(target=self.myShop_add, args=(pages, ))
		myShop.start()


		Eldorado.join()
		WildBerries.join()
		myShop.join()
		# print("end Wilda")
		with self.redisDB.pipeline() as pipe:
			for h_id, hat in self.products.items():
				pipe.hset("products",json.dumps(h_id),json.dumps(hat))
			pipe.execute()
		result = self.redisDB.hgetall('products')
		# print(result)
		# print(result)
		resW = []
		for key in result:
			tmp = result[key].decode('UTF-8')
			resW.append(key.decode('UTF-8'))

			# if json.loads(tmp)['name'].find("Fu") != 1:
			# print(key.decode('UTF-8'), '->', json.loads(tmp)['name'], '->',json.loads(tmp)['brand'],'->',json.loads(tmp)['price'])
		print()
		print("Собрано",len(resW),"единиц товара. ")
		# 		resW.append(json.loads(tmp)['name'])
		# resW.sort()
		# print(resW)


		# print(self.products)
		# 
		# self.connect.commit()
		# print("commit")
		# self.connect.close()
		self.redisDB.close()
		# self.redisDB.bgsave()
		print("close")


		# ТЕСТ ЗАПРОСЫ
Create_a_database_based_on_the_search_query('мыло').search_start(25) # PAGES
Create_a_database_based_on_the_search_query('мясо').search_start(25)
Create_a_database_based_on_the_search_query('мясорубка').search_start(25)
Create_a_database_based_on_the_search_query('ключ').search_start(25)
Create_a_database_based_on_the_search_query('игла').search_start(25)
Create_a_database_based_on_the_search_query('рот').search_start(25)
Create_a_database_based_on_the_search_query('губка').search_start(25)
Create_a_database_based_on_the_search_query('чашка').search_start(25)
Create_a_database_based_on_the_search_query('нитки').search_start(25)
Create_a_database_based_on_the_search_query('краска').search_start(25)
# Create_a_database_based_on_the_search_query('рубашка').search_start()
# Create_a_database_based_on_the_search_query('поиска').search_start()
# Create_a_database_based_on_the_search_query('машина').search_start()
# Create_a_database_based_on_the_search_query('сказка').search_start()
# Create_a_database_based_on_the_search_query('Поиск').search_start()
# Create_a_database_based_on_the_search_query('Машина').search_start()
# Create_a_database_based_on_the_search_query('а').search_start()
# Create_a_database_based_on_the_search_query('оружие').search_start()
# Create_a_database_based_on_the_search_query('стрельба').search_start()
# Create_a_database_based_on_the_search_query('книга').search_start()
print('end')
print('Завершил сеанс за ', (datetime.datetime.now() - start))

# 7-8 сек на 3к товара, 25 стр 3 магазина -> нужно 3-4 сек
