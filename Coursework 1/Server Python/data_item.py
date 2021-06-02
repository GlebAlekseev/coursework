import requests
from fake_headers import Headers
import json

class DataItem():
	def __init__(self):
		self.session = requests.Session()
		headers = Headers(
		        browser="chrome",
		        os="win", 
		        headers=True 
		   		)	
		self.session.headers = headers.generate()
		self.links = [  ['https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?spp=0&pricemarginCoeff=1.0&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=ru&lang=ru&curr=rub&nm=IDS;',"W_iD"],
						['https://api.retailrocket.net/api/1.0/partner/5ba1feda97a5252320437f20/items/?itemsIds=IDS&stock=&format=json',"E_iD"],
						['https://my-shop.ru/cgi-bin/shop2.pl?q=product&id=IDS',"M_iD"]]
		self.result = []



	


	def get(self,Mid):
		for link,prefix in self.links:
			sd=0
			if str(Mid).find(prefix) != -1: 
				try:
					url = link.replace("IDS",Mid[4:])	
					res = self.session.get(url=url)
					res.raise_for_status()
				except requests.exceptions.HTTPError:
					break
									
				sd = json.loads(res.text)
				if prefix == "W_iD":
					name = sd["data"]["products"][0]["name"]
					brand = sd["data"]["products"][0]["brand"]
					price = int(sd["data"]["products"][0]["priceU"])/100
					smart_id = str(sd["data"]["products"][0]["id"])[0:-4] +4*"0"
					url_img = "https://images.wbstatic.net/c516x688/new/"+str(smart_id)+"/"+str(sd["data"]["products"][0]["id"])+"-1.jpg"
					url_profile = "https://www.wildberries.ru/catalog/"+str(sd["data"]["products"][0]["id"]) +"/detail.aspx?"
					url_logo_brand = "https://images.wbstatic.net/brands/small/new/" + str(sd["data"]["products"][0]["siteBrandId"])+ ".jpg"

				if prefix == "M_iD":
					name = str(sd["product"]["ga_item"]["name"])
					brand = str(sd["product"]["ga_item"]["brand"])
					price = str(sd["product"]["ga_item"]["price"])
					url_img = "http://" + str(sd["product"]["images"][0]["preview"]["href"])
					url_profile = "https://my-shop.ru/shop/product/"+str(sd["product"]["ga_item"]["id"])+".html"
					url_logo_brand = ""

				if prefix == "E_iD":
					if len(sd) == 0:
						continue
					name = sd[0]["Name"]
					brand = sd[0]["Model"]
					price = sd[0]["Price"]
					url_img = sd[0]["PictureUrl"]
					url_profile = sd[0]["Url"]
					url_logo_brand = ""
			try:
				self.result.append({'Mid':Mid,'name':name,'brand':brand,'price':price,'url_img':url_img,'url_profile':url_profile,'url_logo_brand':url_logo_brand})
			except UnboundLocalError:
				print("None__")
				continue
		return self.result

