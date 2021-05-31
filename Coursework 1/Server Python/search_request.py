import requests
import config as c
import redis
from fake_headers import Headers
from threading import Thread, Lock
import json
import time
import bs4
import urllib3
import certifi
import urllib.parse


class Create_a_database_based_on_the_search_query:
	def __init__(self,request_name,New_updated_data=[],links_storage = c.Links_storage):
		self.New_updated_data=New_updated_data
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
		self.products = {}

	def get_more_suggestions(request_text):
		df = request_text.split(" ")
		finSug = []
		for el in df:
			newurl = 'https://wbxsearch.wildberries.ru/suggests/common?query=REQUEST'.replace("REQUEST",str(el))

			session = requests.Session()
			headers= Headers(
		        browser="chrome",
		        os="win", 
		        headers=True 
		    	)
			session.headers = headers.generate()

			lst_req_text = request_text.split(" ")

			res = session.get(url=newurl)
			res.raise_for_status()
			suggestions = json.loads(res.text)
			
			for item in suggestions:
				vector_sg = str(item["name"]).split(" ")
				# print(item)
				for inItem in vector_sg:
					for el in lst_req_text:
						if inItem.find(el) != -1:
							finSug.append(inItem)

		return finSug


	def WildBerries_add(self,a):
		newurl = self.links_storage['Wildberries'][0].replace("REQUEST",str(self.request_name))
		res = self.session.get(url=newurl)
		res.raise_for_status()
		data_find_filters_decode = []
		data_find_filters_decode = json.loads(res.text)
		if len(data_find_filters_decode) == 0: # Пустой ответ от Wildberries
			print("Ничего не найдено Wildberries")
			# идет запрос на 'https://www.wildberries.ru/search/brands-suggest?query=REQUEST' - 	suggestions	 рекурсивно вызываю запрос 
			df = self.request_name.split(" ")
			for el in df:
				newurl = 'https://wbxsearch.wildberries.ru/suggests/common?query=REQUEST'.replace("REQUEST",str(el))

			res = self.session.get(url=newurl)
			res.raise_for_status()
			self.suggestions = json.loads(res.text)
			# print("QQQQ",self.suggestions)

			for item in self.suggestions:
				# print(item["name"])
				Create_a_database_based_on_the_search_query(item["name"],self.New_updated_data).search_start(a,self.Wild,self.ELD,self.MShop)



		else:
			i=0
			# print("gjbcr")
			page_threads = []
			def PageInWild_d(a):
				if data_find_filters_decode["query"].find("subject=") != -1:
					newurl = self.links_storage['Wildberries'][2].replace("PAGE",str(i+1)).replace("SHARD",str(data_find_filters_decode["shardKey"])).replace("SUBJECT",str(data_find_filters_decode["query"])).replace("NAME",str(data_find_filters_decode["name"]))
				elif data_find_filters_decode["query"].find("preset=") != -1:
					newurl = self.links_storage['Wildberries'][1].replace("PAGE",str(i+1)).replace("BUCKET",str(data_find_filters_decode["shardKey"])).replace("PRESET",str(data_find_filters_decode["query"]))
				else:
					return # Неудачный запрос
				
				try:
					res = self.session.get(url=newurl)
				except requests.exceptions.ConnectionError:
					print("error: connection closed №a=", a)
					return



				data_decode = []
				try:
					data_decode = json.loads(res.text)
				except json.decoder.JSONDecodeError:
					return
				
				last_history = str(time.time())
				if len(data_decode['data']['products']) == 0:
					pass
				u = 0
				for item in data_decode['data']['products']:
					u+=1
					if self.st == -2:
						self.New_updated_data.append({'id':'W_iD'+str(item["id"]),'price':item["priceU"],'last_history':last_history})
						continue
					smart_id = str(item["id"])[0:-4] +4*"0"
					url_profile = "https://www.wildberries.ru/catalog/"+str(item["id"]) +"/detail.aspx?"
					url_brand_logo = "https://images.wbstatic.net/brands/small/new/" + str(item["siteBrandId"])+ ".jpg"
					url_img =  "https://images.wbstatic.net/c516x688/new/"+str(smart_id)+"/"+str(item["id"])+"-1.jpg"
					# print("=======",item["sale"],"=======")
					# print(item["sale"])
					# print(item["salePriceU"])
					self.products.update({'W_iD'+str(item["id"]):	{'id':item["id"],'name':item["name"],'brandId':item["brandId"],'subjectId':item["subjectId"],
																			 'brand':item["brand"],'sale':str(int(item["sale"])),'price':str(int(item["salePriceU"])/100),'price_full':str(int(item["priceU"])/100),
																			 'pics':item["pics"],'rating':item["rating"],'feedbacks':item["feedbacks"],
																			 'last_history':last_history,
																			 'url_profile':url_profile, 'url_brand_logo':url_brand_logo,
																			 'url_img':url_img
																		 					}})

			if a==-1:
				newurl = 'https://www.wildberries.ru/catalog/0/search.aspx?&search=REQUEST'.replace("REQUEST",str(self.request_name))
				res = self.session.get(url=newurl)
				soup = bs4.BeautifulSoup(res.text, 'lxml')
				container = soup.select('span.goods-count.j-goods-count')
				# print("container",container)
				max_items = ''.join([i for i in str(container) if i.isdigit()])
				
				if str(max_items).isdigit():
					a=int(max_items)/100 *0.8
				else:
					a = 5
			else:
				a=a*0.92

			if a >250:
				a=250
				
			# print("max item",a)
			while i<int(a):
				# print(i)
				
				page_threads.append(Thread(target=PageInWild_d, args=(i, )))
				page_threads[i].start()
				time.sleep(0.01)
				i+=1
			j=0
			for page_th in page_threads:
				page_th.join()
				j+=1



	def Eldorado_add(self,a): # Добавить доп ячейки и добав в БД

			urlHowmuchPages = 'https://www.eldorado.ru/search/catalog.php?q=' + self.request_name
			tmpPgs= self.session.get(url=urlHowmuchPages)
			tmpPgs.raise_for_status()
			soup = bs4.BeautifulSoup(tmpPgs.text, 'lxml')
			container = soup.select('p.Wi') # не стабильно
			Max_pages ="10"

			# print(container,"container Max_Pages")
			# print(Max_pages,"Max_Pages")
			if not Max_pages.isdigit() :
				print("Ничего не найдено Eldorado")
				return

			newurl = self.links_storage['eldorado'][0].replace("REQUEST",str(self.request_name))
			i=0
			page_threads = []
			def PageInEld_d(a):
				newurl_In = newurl.replace("PAGE",str(i*50))
				res = self.session.get(url=newurl_In)
				res.raise_for_status()
				data_find_filters_decode = []
				data_find_filters_decode = json.loads(res.text)
				last_history = str(time.time())
				if len(data_find_filters_decode['data']) == 0:


					return
				u=0

				for item in data_find_filters_decode['data']:
					u+=1
					if self.st == -2:
						self.New_updated_data.append({'id':'E_iD'+str(item["id"]),'price':item["price"],'last_history':last_history})
						continue

					url_profile = "https://www.eldorado.ru/cat/detail/"+str(item["code"])
					try:
						url_img = "https://static.eldorado.ru"+str(item["images"][0]["url"])
					except IndexError:
						url_img=0

					self.products.update({'E_iD'+str(item["id"]):	{'id':item["id"],'name':item["name"],'brand':item["brandName"],'productIdd':item["productId"],
																	 'shortName':item["shortName"],'oldPrice':item["oldPrice"],'price':str(int(item["price"])),'rating':item["rating"],
																			 'last_history':last_history,'feedbacks':item['numOfComment'],
																			 'url_profile':url_profile,'url_img':url_img
																			 					}})

			if a == -1 or a>int(Max_pages):

				a = int(Max_pages)/50 + 1

			# print(a)
			while i<a:
				# print("F")
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
					self.New_updated_data.append({'id':'M_iD'+str(item['ga_item']['id']),'price':item["cost"],'last_history':last_history})
					continue
				# if delete_tr:
				# 		print(item)
				# 		delete_tr = 0
				url_profile = "https://my-shop.ru/shop/product/"+str(item["product_id"])+".html"
				url_img = "http://" + str(item["image"]["href"][2:])
				# print(url_profile)
				# print(url_img)
				self.products.update({'M_iD'+str(item['ga_item']['id']):	{'id':item['ga_item']['id'],'name':item['title'],'brand':item['ga_item']['brand'],'productIdd':item['product_id'],
																	 'price':str(int(item["cost"])),
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
		# print("start",resp.data.decode('utf-8'),"end")
		data = json.loads(resp.data.decode('utf-8'))
		# print(a)
		# print(data['meta']['total']/40)
		if int(data['meta']['total']) == 0:
			print("Ничего не найдено myShop")

			# идет запрос на 'https://www.wildberries.ru/search/brands-suggest?query=REQUEST' - 	suggestions	 рекурсивно вызываю запрос 
			df = self.request_name.split(" ")
			for el in df:
				newurl = 'https://wbxsearch.wildberries.ru/suggests/common?query=REQUEST'.replace("REQUEST",str(el))

			res = self.session.get(url=newurl)
			res.raise_for_status()
			self.suggestions = json.loads(res.text)
			# print("QQQQ",self.suggestions)

			for item in self.suggestions:
				# print(item["name"])
				Create_a_database_based_on_the_search_query(item["name"],self.New_updated_data).search_start(a,self.Wild,self.ELD,self.MShop)



			
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









	def search_start(self,pages=10,Wild=True,ELD=True,MShop=False): # если -1 pages то парсит полностью
		self.Wild= Wild
		self.ELD= ELD
		self.MShop= MShop
		# print("serarch start",self.New_updated_data)

		# print("INITSEARCH")
		# self.get_positions()

		self.st = 0
		if pages == -2:
			self.st = pages
			pages = -1
		# Получение активных запросов
		requests_names = self.redisDB.hgetall('requests_names')
		# print(requests_names)
		resR = []
		for key in requests_names:
			tmp = requests_names[key].decode('UTF-8')
			resR.append(key.decode('unicode_escape'))
		#Проврека на повторный запрос
		status_repeat = False
		# print(resR)
		for req_name in resR:
			# print(req_name)
			if '"'+self.request_name+'"' == req_name:
				# print("REPEAT")
				status_repeat = True
			# print("CHECK = ",'"'+self.request_name+'"' ,"==", req_name)
		if status_repeat and self.st != -2:
			pass
		else:
			#ПАРСИНГ
			# print("pasrsing _")
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


			if self.st == -2:
				# Обновление времени на запросе в общаке
				self.redisDB.close()
				return

			#ВНОС В БД products и requests_names
			with self.redisDB.pipeline() as pipe:
				for h_id, hat in self.products.items():
					pipe.hset("products",json.dumps(h_id),json.dumps(hat))
				pipe.hset("requests_names",json.dumps(str(self.request_name)),json.dumps(str(time.time())))
				pipe.hset("requests_save_names",json.dumps(str(self.request_name)),json.dumps(str(time.time())))
				pipe.execute()



		#ВЫВОД В КОНСОЛЬ
		result = self.redisDB.hgetall('products')
		resW = []
		for key in result:
			tmp = result[key].decode('UTF-8')
			resW.append(key.decode('UTF-8'))

		print("Собрано",len(resW),"единиц товара. По запросу",self.request_name)
		print("serarch end",len(self.New_updated_data))
		self.redisDB.close()
