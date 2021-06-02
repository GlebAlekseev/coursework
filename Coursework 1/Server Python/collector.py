import redis
import time
from threading import Thread, Lock
import config as c
import json

class Collectors: # УДАЛЯЕТ ДАННЫЕ ИЗ БД ДЛЯ ПОИСКА (устаревшие*) Работает каждые 10 мин
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
			time.sleep(60*10) # Каждые 10 мин включается
	# ЗАПУСК Сборщик мусора, Товаров last_history # Каждые 10 мин включается
	def bad_position_collector(self,New_updated_data):
		while True:
			result = self.redisDB.hgetall('products')
			for key in result:
				try:
					left = json.loads(result[key].decode('UTF-8'))['last_history']
				except NameError:
					left = 0
					left = 0

				if float(str(left))+60*10 <time.time():
					
					# Переход в построение истории
					New_updated_data.append({'id':key.decode('UTF-8'),'price':json.loads(result[key].decode('UTF-8'))['price'],'last_history':json.loads(result[key].decode('UTF-8'))['last_history']})# Сейвит ИД, цену, ласт_хистори (потом рейтинг)
					temp = key
					self.redisDB.hdel("products",key)

			print(" осталось ",len(self.redisDB.hgetall('products')))
			time.sleep(60*10)

	def run(self,New_updated_data):
		print("collector starrted")
		# New_updated_data.append("МУСОР")
		Thread_bad_request_collector = Thread(target=self.bad_request_collector, args=(1, ))
		Thread_bad_request_collector.start()

		Thread_bad_position_collector = Thread(target=self.bad_position_collector, args=(New_updated_data, ))
		Thread_bad_position_collector.start()





