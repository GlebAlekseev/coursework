
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


import random
import time
# def write_msg(user_id, message):
#     vk.method('messages.send', {'user_id': user_id, 'message': message})
random.seed(time.time())




        #     request = event.text
        #     if request == "привет":
        #         write_msg(event.user_id, "Хай")
        #     elif request == "пока":
        #         write_msg(event.user_id, "Пока((")
        #     else:
        #         write_msg(event.user_id, "Не поняла вашего ответа...")



class VkNotify():
	def __init__(self, token):
		self.token = token
		self.vk = vk_api.VkApi(token=token)
		self.longpoll = VkLongPoll(self.vk)

	def send(self,message,person):
		# Случай если линка нет, то стоит None
		if person != None:
			user_id = person
			# print(person)
			# print("user_id",user_id)
			try:
				self.vk.method('messages.send', {'user_id':user_id, 'message': message,'random_id':random.randint(1,1000000)})
			except vk_api.exceptions.ApiError:
				print("Превышен лимит кол-ва сообщений")
			
		else:
			print("User_id_vk не указан в настройках")

	def get_last_meassage(self,user_id):
		data = self.vk.method('messages.getHistory', {'count':'1', 'user_id': user_id})
		try:
			return data["items"][0]["text"]
		except IndexError:
			print("Условие не выполнено, отсуствует диалог")
			return "#"

		
		# print(data)

	def is_ValidId(self,id_vk,key):
		if self.get_last_meassage(id_vk) == key:
			return True
		else:
			return False

		# Получить последнее сообщение с ключом
		# Сравнить его с ключом из бд
		# Искать в переписке по иду
