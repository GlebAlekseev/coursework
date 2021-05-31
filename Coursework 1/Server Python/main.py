import requests
import bs4
import datetime
import logging
import re
import os
import platform
from selenium import webdriver
from seleniumwire import webdriver  
import sqlite3
import urllib3
import certifi
import urllib.parse
import copy
import redis
import hashlib
from nickname_generator import generate
from fake_headers import Headers
import time
import json

import random
random.seed(time.time())

import config as c
from search_request import Create_a_database_based_on_the_search_query


from updater import Updating_Master_data,Updating_tracked_data
from collector import Collectors

from vk_notify import VkNotify
import api_vk as c
# from flask import Flask, request, jsonify

# from structure import Structure

#========================================================================================
from data_person import DataPerson
from data_item import DataItem

from flaskserver import FlaskAppWrapper
# from structure import Structure

from flask import Flask, Response, request
	
class MainStream():
	"""docstring for MainStream"""
	def __init__(self):
		self.app = FlaskAppWrapper('app')
		self.New_updated_data = []

		# super(ClassName, self).__init__()

	def checkauth(self):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		try:
			cursor.execute("""CREATE TABLE users
				(id INTEGER PRIMARY KEY, login text, password text,hash text,key text,last_session_update text)
				""")
		except sqlite3.OperationalError:
			print("БД уже создана")
			pass
		else:
			print("Создание БД")
			pass
		# print( Response(status=200, headers={}))
		# print(request.data)


		login = json.loads(request.data.decode('UTF-8'))['login']
		# print(login)
		hash_ = json.loads(request.data.decode('UTF-8'))['hash']
		# print(request.data.decode('UTF-8'))
		hash_time = json.loads(request.data.decode('UTF-8'))['hash_time']
		info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))
		# print("start check")
		if info.fetchone() is None:
			connect.close()	
			# print("104")
			return "104" # Неверный сейв
		else:
			info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))
			for i in info:
				hash_bd = str(i).replace('(','').replace(')','').split(',')[3]
				hash_time_bd = str(i).replace('(','').replace(')','').split(',')[5]
				break
			hash_bd = hash_bd.replace("'",'').strip()
			hash_time_bd = hash_time_bd.replace("'",'').strip()
			if float(time.time()) -60*60*24*30 < float(hash_time_bd):
				# print("h",hash_)
				# print("h_bd",hash_bd)
				if hash_ == hash_bd:
					connect.close()	
					# print("go")
					return "Go"
				else:
					connect.close()	
					# print("106")
					return "106" # Неверный хеш
			else:
				connect.close()	
				print("105")
				return "105" # Устаревший в бд сейв



	def login(self):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		try:
			cursor.execute("""CREATE TABLE users
				(id INTEGER PRIMARY KEY, login text, password text,hash text,key text,last_session_update text)
				""")
		except sqlite3.OperationalError:
			# print("БД уже создана")
			pass
		else:
			# print("Создание БД")
			pass
		login = json.loads(request.data.decode('UTF-8'))['login']
		password = json.loads(request.data.decode('UTF-8'))['password']
		info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))
		# print("start login")
		if info.fetchone() is None:
			connect.close()	
			# print("102")
			return "102" # Неверные данные
		else:
			info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))
			for i in info:
				password_bd = str(i).replace('(','').replace(')','').split(',')[2]
				key_bd = str(i).replace('(','').replace(')','').split(',')[4]
				break
			password_bd = password_bd.replace("'",'').strip()
			key_bd = key_bd.replace("'",'').strip()
			password_curr = hashlib.md5(str(str(password) +str(key_bd) ).encode()).hexdigest()
			if password_curr == password_bd:
				#Новый хеш
				hash_ = hashlib.md5((str(password_bd)+str(key_bd)+str(time.time())).encode()).hexdigest()
				last_session_update = time.time();
				
				cursor.execute('UPDATE users SET hash = ?,last_session_update = ? WHERE login = ?',(hash_,last_session_update,login, ))
				connect.commit()
				connect.close()
				# print("hash_,",hash_)
				return str(hash_)
			connect.close()
			# print("103")
			return "103"


	def register(self):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		try:
			cursor.execute("""CREATE TABLE users
				(id INTEGER PRIMARY KEY, login text, password text,hash text,key text,last_session_update text)
				""")
		except sqlite3.OperationalError:
			# print("БД уже создана")
			pass
		else:
			# print("Создание БД")
			pass
		login = json.loads(request.data.decode('UTF-8'))['login']
		password = json.loads(request.data.decode('UTF-8'))['password']
		info = cursor.execute('SELECT * FROM users WHERE login=?', (login, ))

		if info.fetchone() is None:
			key = hashlib.md5(str(login).encode()).hexdigest()
			password = hashlib.md5(str(str(password) +str(key) ).encode()).hexdigest()
			hash_ = hashlib.md5((str(password)+str(key)+str(time.time())).encode()).hexdigest()
			last_session_update = time.time();
			data = (str(login), str(password),str(hash_),str(key),str(last_session_update)) 
			cursor.execute("INSERT INTO users  (login,password,hash,key,last_session_update)VALUES (?,?,?,?,?)", data)

			connect.commit()
			connect.close()
			DataPerson().set(login)
			return str(hash_)
		else:
			connect.close()
			return "101" # Ошибка: Логин занят



	def changePW(self):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		try:
			cursor.execute("""CREATE TABLE users
				(id INTEGER PRIMARY KEY, login text, password text,hash text,key text,last_session_update text)
				""")
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
			# print(str(i).replace('(','').replace(')','').split(','))
			password_bd = str(i).replace('(','').replace(')','').split(',')[2]
			key_bd = str(i).replace('(','').replace(')','').split(',')[4]
			break
		password_bd = password_bd.replace("'",'').strip()
		key_bd = key_bd.replace("'",'').strip()
		password_curr = hashlib.md5(str(str(curr_password) +str(key_bd) ).encode()).hexdigest()
		if password_curr == password_bd:
			password = hashlib.md5(str(str(new_password) +str(key_bd) ).encode()).hexdigest()
			cursor.execute('UPDATE users SET password = ? WHERE login = ?',(str(password),str(login), ))
			connect.commit()
			connect.close()
			return "Go" # Смена прошла успешно
		else:
			connect.close()
			return "108" # Текущий пароль неверно указан



# ================================================================================= РАБОТА С ПАРСЕРОМ ===============================================================================================


	def search(self):
		# print("DATA+0",len(self.New_updated_data))

		# ДАННЫЕ ИЗ ЗАПРОСА
		request_text = json.loads(request.data.decode('UTF-8'))['request_text'] 
		SORTAZ = json.loads(request.data.decode('UTF-8'))['SORTAZ']
		SORT12 = json.loads(request.data.decode('UTF-8'))['SORT12']
		SHOPW = json.loads(request.data.decode('UTF-8'))['SHOPW']
		SHOPD = json.loads(request.data.decode('UTF-8'))['SHOPD']
		SHOPM = json.loads(request.data.decode('UTF-8'))['SHOPM']
		HOWMUCH = json.loads(request.data.decode('UTF-8'))['HOWMUCH']
		# HOWMUCHP = 10

		print(SHOPW,SHOPD,SHOPM,SORTAZ,SORT12,'HOWMUCH=',HOWMUCH)

		# Create_a_database_based_on_the_search_query(request_text).search_start(HOWMUCHP,SHOPW,SHOPD,SHOPM) # Обновляет позиции в Redis по запросу 
		Create_a_database_based_on_the_search_query(request_text,self.New_updated_data).search_start(HOWMUCH,True,True,True) # Обновляет позиции в Redis по запросу 


		# Получаю данные из бд
		redisDB = redis.Redis(db=1)
		resR=[]
		request_receiveRaw = redisDB.hgetall('products')
		for key in request_receiveRaw:
			tmp = request_receiveRaw[key].decode('UTF-8')
			temp = json.loads(tmp)
			temp["Mid"]= key.decode('unicode_escape').strip('"')
			resR.append(temp)
		for er in resR:
			# print(er)
			pass
		sugst = Create_a_database_based_on_the_search_query.get_more_suggestions(request_text)
		sugst.append(request_text)
		resF = []
		# print("F",sugst)
		for item in resR:
			for sug in sugst:
				if item["name"].find(sug) != -1: # нашло
					if item["Mid"].find("W_iD") != -1 and SHOPW:
						resF.append(item)
					if item["Mid"].find("E_iD") != -1 and SHOPD:
						resF.append(item)
					if item["Mid"].find("M_iD") != -1 and SHOPM:
						resF.append(item)
					break




		def sort_list_data_name(data,ASC = True):
			n = len(data)
			if ASC:
				for i in range(n):
					for j in range(i + 1, n):
						if data[i]["name"] > data[j]["name"]:
							data[i], data[j] = data[j], data[i]
			else:
				for i in range(n):
					for j in range(i + 1, n):
						if data[i]["name"] < data[j]["name"]:
							data[i], data[j] = data[j], data[i]

		def sort_list_data_price(data,ASC = True):
			n = len(data)
			if ASC:
				for i in range(n):
					for j in range(i + 1, n):
						if float(data[i]["price"]) > float(data[j]["price"]):
							data[i], data[j] = data[j], data[i]
			else:
				for i in range(n):
					for j in range(i + 1, n):
						if float(data[i]["price"]) < float(data[j]["price"]):
							data[i], data[j] = data[j], data[i]



		if len(resF)==0:
			resF = []
			for item in resR:
				if item["name"].find(request_text[0:int(len(request_text)/2)]) != -1:
					resF.append(item)
		# СОРТИРУЮ ДАННЫЕ

		sort_list_data_name(resF,SORTAZ) # ASC сортировка
		sort_list_data_price(resF,SORT12) # 12 сортировка
		# ВОЗВРАЩАЮ РЕЗУЛЬТАТ
		# print(resF)
		# print(resF)
		return json.dumps(resF)



	def add_to_tracked(self):
		login = json.loads(request.data.decode('UTF-8'))['login']
		Mid = json.loads(request.data.decode('UTF-8'))['Mid']
		try:
			status_ = json.loads(request.data.decode('UTF-8'))['status_']
		except KeyError:
			status_=False
		status = False
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		try:
			cursor.execute("""CREATE TABLE user_tracking
					(id INTEGER PRIMARY KEY, login text, Mid text, tracking text)
					""")
		except sqlite3.OperationalError:
			# print("БД уже создана")
			pass
		else:
			# print("Создание БД")
			pass
		if status_:
			info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid=?' , (login,Mid ))
			if info.fetchone() is None:
				return "600"
			else:
				return "601"
		info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid=?' , (login,Mid ))
		if info.fetchone() is None:
			data = (login,Mid,False) 
			cursor.execute("INSERT INTO user_tracking (login,Mid,tracking)VALUES (?,?,?)", data)
			connect.commit()
			# print("600")
			return "600"
		else:
			if status:
				pass
				connect.close()
				# print("650")
				return "650"
			else:
				connect.close()
				# print("601")
				return "601"



	def delete_to_tracked(self):
		login = json.loads(request.data.decode('UTF-8'))['login']
		Mid = json.loads(request.data.decode('UTF-8'))['Mid']
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		try:
			cursor.execute("""CREATE TABLE user_tracking
					(id INTEGER PRIMARY KEY, login text, Mid text, tracking text)
					""")
		except sqlite3.OperationalError:
			# print("БД уже создана")
			pass
		else:
			# print("Создание БД")
			pass
		info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid=?' , (login,Mid ))
		if info.fetchone() is None: 
			connect.close()
			return "601"
		else:
			cursor.execute('DELETE FROM user_tracking WHERE login = ? AND Mid=?', (login,Mid ))
			connect.commit()
			connect.close()
			# print("600")
			return "600"


	def get_tracked(self):
		request_text = json.loads(request.data.decode('UTF-8'))['request_text'] 

		SORTAZ = json.loads(request.data.decode('UTF-8'))['SORTAZ'] 
		SORT12 = json.loads(request.data.decode('UTF-8'))['SORT12'] 
		SHOPW = json.loads(request.data.decode('UTF-8'))['SHOPW'] 
		SHOPD = json.loads(request.data.decode('UTF-8'))['SHOPD'] 
		SHOPM = json.loads(request.data.decode('UTF-8'))['SHOPM'] 
		login = json.loads(request.data.decode('UTF-8'))['login']
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		try:
			cursor.execute("""CREATE TABLE user_tracking
					(id INTEGER PRIMARY KEY, login text, Mid text, tracking text)
					""")
		except sqlite3.OperationalError:
			# print("БД уже создана")
			pass
		else:
			# print("Создание БД")
			pass
		resF= []
		info = cursor.execute('SELECT * FROM user_tracking WHERE login=?' , (login,))
		if info.fetchone() is None:  # Добавление 
			return "701" # В отслежке пусто
		else:# Уже добавлен
			info = cursor.execute('SELECT * FROM user_tracking WHERE login=?' , (login,))
			for item in info:
				if SHOPW and str(item[2]).find("W_iD") !=-1:
					# print("W")
					resF.append(item)
				if SHOPD and str(item[2]).find("E_iD") !=-1:
					# print("E")
					resF.append(item)
				if SHOPM and str(item[2]).find("M_iD") !=-1:
					# print("M")
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
					if len(sd) == 0:
						continue
					Mid = 'E_iD'+str(sd[0]["ItemId"])
					# print(sd,"Eid")
					name = sd[0]["Name"]
					brand = sd[0]["Model"]
					price = sd[0]["Price"]
					url_img = sd[0]["PictureUrl"]
					url_profile = sd[0]["Url"]


				if str(item[2]).find("M_iD") != -1:
					newurl = url_M.replace("IDS",str(item[2])[4:])
					res = session.get(url=newurl)
					res.raise_for_status()
					sd = json.loads(res.text)

					Mid = 'M_iD'+str(sd["product"]["ga_item"]["id"])
					name = str(sd["product"]["ga_item"]["name"])
					brand = str(sd["product"]["ga_item"]["brand"])
					price = str(sd["product"]["ga_item"]["price"])
					url_img = "http://" + str(sd["product"]["images"][0]["preview"]["href"])
					url_profile = "https://my-shop.ru/shop/product/"+str(sd["product"]["ga_item"]["id"])+".html"
					url_logo_brand = ""


				if len(sd) == 0:
					continue
				fin_data_checked.append((Mid,name,brand,price,url_img,url_profile,url_logo_brand))	
		get_data(resF)
		connect.close()
		# redisDB = redis.Redis(db=1)
		def sort_list_data_name(data,ASC = True):
			n = len(data)
			if ASC:
				for i in range(n):
					for j in range(i + 1, n):
						if data[i][1] > data[j][1]:
							data[i], data[j] = data[j], data[i]
			else:
				for i in range(n):
					for j in range(i + 1, n):
						if data[i][1] < data[j][1]:
							data[i], data[j] = data[j], data[i]

		def sort_list_data_price(data,ASC = True):
			n = len(data)
			if ASC:
				for i in range(n):
					for j in range(i + 1, n):
						if float(data[i][3]) > float(data[j][3]):
							data[i], data[j] = data[j], data[i]
			else:
				for i in range(n):
					for j in range(i + 1, n):
						if float(data[i][3]) < float(data[j][3]):
							data[i], data[j] = data[j], data[i]
		# for item in fin_data_checked:
			# print(item)

		sort_list_data_name(fin_data_checked,SORTAZ) # ASC сортировка
		sort_list_data_price(fin_data_checked,SORT12) # 12 сортировка
		return json.dumps(fin_data_checked )


	def get_history(self):
		Mid = json.loads(request.data.decode('UTF-8'))['Mid']
		connect = sqlite3.connect("data.db")
		connect.isolation_level= 'DEFERRED'
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
			return "801"
		else:
			info = cursor.execute('SELECT * FROM items_history WHERE id=?', (Mid, ))
			dataH = info.fetchall()
			for item in dataH:
				history_items.append((item[0],item[1],item[2]))	
				break
			connect.close()
			# print(history_items)
			return json.dumps(history_items)



	def tracking(self):
		# print( "==================================================")
		login = json.loads(request.data.decode('UTF-8'))['login'] 
		Mid = json.loads(request.data.decode('UTF-8'))['Mid'] 
		is_set = json.loads(request.data.decode('UTF-8'))['is_set']
		if is_set:
			bool_ = json.loads(request.data.decode('UTF-8'))['bool']
			# print("=======================bool_",bool_)
		# print("=================here1", is_set)

		if is_set: # устанвоить 
			# print("set")
			st = DataPerson().set_tracking_status(login,Mid,bool_)
			# print(st,"st _ set")
			return st
		else: # вернуть текщуее состояние
			st = DataPerson().get_tracking_status(login,Mid)
			# print(st,"get")
			return st

	def get_parse_page(self):
		# print("connect")
		
		try:
			login = json.loads(request.data.decode('UTF-8'))['login'] 
		except Exception as e:
			print(json.loads(request.data.decode('UTF-8')))


		data=DataPerson().get(login)
		# print(data[1])
		return data[1]

	def set_parse_page(self):
		login = json.loads(request.data.decode('UTF-8'))['login'] 
		count = json.loads(request.data.decode('UTF-8'))['count'] 
		data=DataPerson().edit(login,pages=count)
		return "91"
	

	def set_style(self):
		login = json.loads(request.data.decode('UTF-8'))['login'] 
		wild = json.loads(request.data.decode('UTF-8'))['wild']
		mshop = json.loads(request.data.decode('UTF-8'))['mshop']
		eldorado = json.loads(request.data.decode('UTF-8'))['eldorado']
		stl = str(wild)+";" +str(mshop)+";" +str(eldorado)
		DataPerson().edit(login,style=stl)
		return "92"
	def get_style(self):
		login = json.loads(request.data.decode('UTF-8'))['login'] 


		style = DataPerson().get(login)[2]
		styleL = style.split(";")
		return json.dumps(styleL)



	def add_item_to_tracking_from_link(self):
		login = json.loads(request.data.decode('UTF-8'))['login'] 
		link = json.loads(request.data.decode('UTF-8'))['link'] 
		Mid = []
		print(login,link)
		# Mid
		if link.find("wildberries") != -1:
			Mid = "W_iD" + str(link.split("/")[4])

		if link.find("my-shop.ru") != -1:
			Mid = "M_iD"+str(link.split("/")[-1].split(".")[0])

		if link.find("eldorado.ru") != -1:
			session = requests.Session()
			headers= Headers(
	        browser="chrome",
	        os="win", 
	        headers=True 
	    	)
			session.headers = headers.generate()
			res = session.get(url=link)
			res.raise_for_status()
			content = json.loads(res.text)
			soup = bs4.BeautifulSoup(content, 'lxml')
			Mid = "E_iD" + str(soup.select('span.sku'))

		try:
			data = DataItem().get(Mid)
		except IndexError:
			# print("Пропуск", Mid)
			return "213"

		
			# сделать dateitem гет b try есл иошибка то выход с 213
		# Доабвление по миду и логину в  отслежку
		# print("Mid",Mid)
		if len(Mid) != 0:
			if DataPerson().insert_Mid(login,Mid) == "220":
				# print("210")
				dat = data[0]["name"] +"/"+data[0]["brand"]
				return dat
			else:
				# print("211")
				return "211"
		# print("212")
		return "212"
				

	def get_keyVk(self,login=None): 
		if login == None:
			login = json.loads(request.data.decode('UTF-8'))['login'] 
		# Узнает есть ли ключ, если нет то доабвляет и возвращает его же
		SLO = "102030405060708090A0B0C0D0E0F0G0H0J0Y0T0R0E0V0L"
		x = SLO.split("0")
		# print("***",SLO.split("0"))
		
		key = ''.join(random.sample(x,len(x)))

		# генерирование ключа
		data = DataPerson().get(login)[4]

		if data is None:
			DataPerson().edit(login,key_=key)
		else:
			key = data
		return key


	def set_vkId(self):
		login = json.loads(request.data.decode('UTF-8'))['login'] 
		id_vk = json.loads(request.data.decode('UTF-8'))['id_vk'] 
		if VkNotify(c.token).is_ValidId(id_vk,self.get_keyVk(login)):
			DataPerson().edit(login,link_vk=id_vk)
			VkNotify(c.token).send("Привет, "+str(login)+", я Сергей",id_vk)
			return "710"
		else:
			return "711"
	def get_vkId(self):
		# print("start get vkid")
		login = json.loads(request.data.decode('UTF-8'))['login'] 
		# print(login)
		if DataPerson().get(login)[3] is None:
			return "721"
		else:
			if len(DataPerson().get(login)[3]) !=0:
				dat = DataPerson().get(login)[3]
				return dat
			else:
				return "721"
			

		


	def run(self):
		# Перечисление ожидаемых линков
		self.app.add_endpoint(endpoint='/checkauth', endpoint_name='checkauth', handler=self.checkauth)
		self.app.add_endpoint(endpoint='/login', endpoint_name='login', handler=self.login)
		self.app.add_endpoint(endpoint='/register', endpoint_name='register', handler=self.register)
		self.app.add_endpoint(endpoint='/changepw', endpoint_name='changepw', handler=self.changePW)


		self.app.add_endpoint(endpoint='/search', endpoint_name='search', handler=self.search)
		self.app.add_endpoint(endpoint='/add_to_tracked', endpoint_name='add_to_tracked', handler=self.add_to_tracked)
		self.app.add_endpoint(endpoint='/delete_to_tracked', endpoint_name='delete_to_tracked', handler=self.delete_to_tracked)
		self.app.add_endpoint(endpoint='/get_tracked', endpoint_name='get_tracked', handler=self.get_tracked)
		self.app.add_endpoint(endpoint='/get_history', endpoint_name='get_history', handler=self.get_history)

		self.app.add_endpoint(endpoint='/tracking', endpoint_name='tracking', handler=self.tracking)
		self.app.add_endpoint(endpoint='/get_parse_page', endpoint_name='get_parse_page', handler=self.get_parse_page)
		self.app.add_endpoint(endpoint='/set_parse_page', endpoint_name='set_parse_page', handler=self.set_parse_page)
		
		self.app.add_endpoint(endpoint='/add_item_to_tracking_from_link', endpoint_name='add_item_to_tracking_from_link', handler=self.add_item_to_tracking_from_link)

		self.app.add_endpoint(endpoint='/set_style', endpoint_name='set_style', handler=self.set_style)

		self.app.add_endpoint(endpoint='/get_style', endpoint_name='get_style', handler=self.get_style)

		self.app.add_endpoint(endpoint='/get_vkId', endpoint_name='get_vkId', handler=self.get_vkId)
		self.app.add_endpoint(endpoint='/set_vkId', endpoint_name='set_vkId', handler=self.set_vkId)

		self.app.add_endpoint(endpoint='/get_keyVk', endpoint_name='get_keyVk', handler=self.get_keyVk)

		Collectors().run(self.New_updated_data)
		Updating_tracked_data().run()
		# Updating_Master_data().run(self.New_updated_data) # NewData это данные которые нужно сохранять # ИСПОЛЬЗОВАТЬ ТОЛЬКО КОГДА ИСПРАВЛЮ ПОДБОР КЛЮЧ СЛОВ ПОИСКА





		# print("start")
		
		self.app.start()

		# ЗАПУСК МОДУЛЕЙ СЕРВЕРА
		# Запускает апдейтер и коллектор







print(__name__,"NAME")



if __name__ == '__main__':
	# print("main")
	# Updating_Master_data().run() 
	MainStream().run()

	 # Удаляет плохие данные
	# Обновляет данные
	# app.run(debug=True, port=5000,threaded=True) # Ожидает запросы с клиента 
