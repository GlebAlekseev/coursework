import sqlite3
import requests
from fake_headers import Headers
import json

from data_item import DataItem
from data_person import DataPerson

import api_vk as c
from vk_notify import VkNotify
class Notify():
	def __init__(self,Mid):
		self.Mid = Mid
		
	def send_to_user(self,NewPrice,OldPrice):
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
		cursor.execute('SELECT * FROM user_tracking WHERE tracking=? AND Mid=?',(0,self.Mid,) )
		subscribers = cursor.fetchall() # Подписчики на item

		if subscribers is None:
			return # НИкто не подписан на item
		else:
			if DataItem().get(self.Mid) == None:
				return
			data = DataItem().get(self.Mid)[0]
			

			for sub in subscribers:
				person = DataPerson().get(sub[1])
				# print("in_notify",person)
				# print("self.Mid",self.Mid)
				# print("NewPrice",NewPrice)
				# print("OldPrice",OldPrice)
				# print("date[name]",data["name"])
				# print("date[brand]",data["brand"])
				# print("date[url_profile]",data["url_profile"])

				message = "Изменилась цена товара на "+str(int(NewPrice)-int(OldPrice))+"₽"+ "\nЦена: "+str(OldPrice)+"₽" + " --> " + str(NewPrice)+"₽ \nНазвание: "+data["name"]+"/"+data["brand"]+ "\nПерейти: "+ data["url_profile"]
				VkNotify(c.token).send(message,person[3])# передаеются настройки 



			# Получение данных о товаре



		# Получает список подписчиков, логины
		# Если логинов 0 то конец
		# Иначе получает аднные о товаре

		# Получаю таблицу пользователей и их настроек 
		# Циколм проходится по логинам и одновременно выношу настройки уведмолений, в частности ссылки куда, статусы, количества и тд
		# Проходя циклом вызываю класс соотвествующий методу уведомления, класс вк, передаю в него ссылку куда, сообщение, и команду send