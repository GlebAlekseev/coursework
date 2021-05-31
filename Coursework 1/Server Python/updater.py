from threading import Thread, Lock
import time
import redis
import sqlite3
from search_request import Create_a_database_based_on_the_search_query
import requests
from fake_headers import Headers
import json


from notifications import Notify
class Updating_Master_data:
	def __init__(self):
		pass
	def processing_all_requests(self,New_updated_data):
		self.New_updated_data=New_updated_data
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

			InsertInto_data = []
			Update_data = []
			print("aLL",len(result))
			for key in result:
				tmp = result[key].decode('UTF-8')
				if float(tmp.strip('"'))+60*60*12/(12*60) < time.time(): # если данные не обновлялись 12 часов
					# print(key.decode('unicode_escape').strip('"'))
					# Обновление времени обновления по запросу
					print(key.decode('unicode_escape').strip('"'))
					Create_a_database_based_on_the_search_query(key.decode('unicode_escape').strip('"'),New_updated_data).search_start(-2) #  -2 значит полностью, внутри функции добавляет в массив
					if len(self.New_updated_data) > 7000: # превышает 10к
						# Запрос на бд, получение всей истории
						cursor.execute('SELECT * FROM items_history')
						Data_DB = cursor.fetchall()
						# провести подмены, и данные которые обнвоились добавить в отдельный массив
						for elementNEW in self.New_updated_data:
							is_available = 1
							for elementDB in Data_DB:
								if elementDB[0] == elementNEW["id"]: # ЕСЛИ ЕСТЬ В БД
									history = str(elementDB[2]) + '\n' + elementNEW['last_history']
									price = str(elementDB[1]) + '\n' + str(elementNEW['price'])
									Update_data.append({'id':elementNEW["id"],'price':price,'last_history':history})
									is_available = 0
									
							if is_available: # Если нет в БД
								InsertInto_data.append(elementNEW)
									# Добавить в insert

				if len(InsertInto_data)>100000:
						# Внос новых данных
						i = 0
						for el in InsertInto_data:
							# print(i,"",len(InsertInto_data))
							cursor.execute("INSERT INTO items_history VALUES (?,?,?)", (el["id"],el["price"],el["last_history"],))
							i+=1
						InsertInto_data.clear()

				if len(Update_data)>100000:
						j = 0
						for el in Update_data:
							# print(i,"",len(Update_data))
							cursor.execute('UPDATE items_history SET  price = ?,last_history = ? WHERE id = ?',(el["price"],el["last_history"],el["id"],))
							j+=1
						Update_data.clear()

			# ВНОС В БД данных
			if len(InsertInto_data)>0:
				# Внос новых данных
				for el in InsertInto_data:
					cursor.execute("INSERT INTO items_history VALUES (?,?,?)", (el["id"],el["price"],el["last_history"],))

			if len(Update_data)>0:
				for el in Update_data:
					cursor.execute('UPDATE items_history SET  price = ?,last_history = ? WHERE id = ?',(el["price"],el["last_history"],el["id"],))
				# Обновление старых данных
			self.New_updated_data.clear()
			connect.commit()
			connect.close()		
			time.sleep(60*60*6) # Каждые 12 часов

	def run(self,New_updated_data):
		# print("run updater")
		Thread_updating_information = Thread(target=self.processing_all_requests, args=(New_updated_data, ))
		Thread_updating_information.start()






class Updating_tracked_data:
	def __init__(self):
		pass
	def processing_(self,a):
		while True:
			# print("start check tracked")
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
			cursor.execute('SELECT * FROM user_tracking WHERE tracking=?',(0,))
			Tracked_data = cursor.fetchall()
			session = requests.Session()
			headers = Headers(
		        browser="chrome",
		        os="win", 
		        headers=True 
		   		)	
			session.headers = headers.generate()
			INSERT_arr = []
			UPDATE_arr = []
			# Формирование новых данных
			for data in Tracked_data:
				# print(data[2])
				# Составление на основе Mid ссылки и получени ответа request
				if str(data[2]).find("W_iD") != -1: # Если Wildberries
					url = 'https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?spp=0&pricemarginCoeff=1.0&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=ru&lang=ru&curr=rub&nm=IDS;'.replace("IDS",data[2][4:])
				if str(data[2]).find("E_iD") != -1: # Если Eldorado
					url = 'https://api.retailrocket.net/api/1.0/partner/5ba1feda97a5252320437f20/items/?itemsIds=IDS&stock=&format=json'.replace("IDS",data[2][4:])
				if str(data[2]).find("M_iD") != -1: # Если Myshop
					url = 'https://my-shop.ru/cgi-bin/shop2.pl?q=product&id=IDS'.replace("IDS",data[2][4:])
				res = session.get(url=url)
				res.raise_for_status()
				sd = json.loads(res.text)
				if str(data[2]).find("W_iD") != -1:
					Mid = 'W_iD'+str(sd["data"]["products"][0]["id"])
					price = int(sd["data"]["products"][0]["priceU"])/100
						
				if str(data[2]).find("E_iD") != -1:
					if len(sd) == 0:
						continue
					Mid = 'E_iD'+str(sd[0]["ItemId"])
					price = sd[0]["Price"]
	
				if str(data[2]).find("M_iD") != -1:
					Mid = 'M_iD'+str(sd["product"]["ga_item"]["id"])
					price = str(sd["product"]["ga_item"]["price"])


				info = cursor.execute('SELECT * FROM items_history WHERE id = ?',(Mid,)) 
				if info.fetchone() is  None:
					pass
				else:
					#Получить цену из БД, если позиции с идом нету то пропуск
					info = cursor.execute('SELECT * FROM items_history WHERE id = ?',(Mid,))
					forPriceInf = info.fetchall()
					for ele in forPriceInf:
						OldPriceList = ele[1].split("\n")
						OldPriceSize = len(ele[1].split("\n"))
						OldPrice = int(float(OldPriceList[OldPriceSize-1]))

					# print(OldPrice)
					# print("До Chech")
					pricez = int(float(price))
					if float(pricez) != float(OldPrice): # Если цена текущая не равна прошлой,  в iem_hist по иду data[2] найти айтем
						# pass
						# Вызов уведомителя
						# print("#CHECK",pricez,OldPrice)
						Notify(Mid).send_to_user(pricez,OldPrice)
						# Передает ид, и две цены (до и после),

				info = cursor.execute('SELECT * FROM items_history WHERE id = ?',(Mid,))

				timeN = time.time()
				if info.fetchone() is None: 
					history = timeN
					INSERT_arr.append({'id':data[2],'last_history':history,'price':price})
				else:
					info = cursor.execute('SELECT * FROM items_history WHERE id = ?',(Mid,))
					elementDB = info.fetchall()
					for element in elementDB:
						history = str(element[2]) + '\n' + str(timeN)
						price = str(element[1]) + '\n' + str(price)
					UPDATE_arr.append({'id':data[2],'last_history':history,'price':price})
			if len(INSERT_arr)>0:
				# Внос новых данных
				for el in INSERT_arr:
					cursor.execute("INSERT INTO items_history VALUES (?,?,?)", (el["id"],el["price"],el["last_history"],))
			if len(UPDATE_arr)>0:
				for el in UPDATE_arr:
					cursor.execute('UPDATE items_history SET  price = ?,last_history = ? WHERE id = ?',(el["price"],el["last_history"],el["id"],))
					# Обновление старых данных
			# print("final check tracked")
			connect.commit()
			connect.close()		
			time.sleep(60*5) # Каждые 12 часов






	def run(self):
		# print("start update tracked")
		Thread_tracked_information = Thread(target=self.processing_, args=(1, ))
		Thread_tracked_information.start()

