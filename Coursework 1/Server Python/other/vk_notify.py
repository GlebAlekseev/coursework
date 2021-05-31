import api_vk as c

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


import random
import time
# def write_msg(user_id, message):
#     vk.method('messages.send', {'user_id': user_id, 'message': message})
from messages import Message
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

	def handler(self):
		for event in self.longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW:
				if event.to_me:
					if event.text.upper() == "Справка".upper():
						self.vk.method('messages.send', {'user_id':event.user_id, 'message': Message(event.user_id,0).handler_(),'random_id':random.randint(1,1000000)})
					elif event.text.upper() == "Отслеживаемое".upper():
						self.vk.method('messages.send', {'user_id':event.user_id, 'message': Message(event.user_id,1).handler_(),'random_id':random.randint(1,1000000)})


					elif event.text.upper() == "Добавить /link".upper():
						print("Добавить /link")
					elif event.text.upper() == "Добавить Mid".upper():
						print("Добавить /link")
					elif event.text.upper() == "Удалить /link".upper():
						print("Удалить /link")
					elif event.text.upper() == "Удалить Mid".upper():
						print("Удалить Mid")
					elif event.text.upper() == "Удалить все".upper():
						print("Удалить все")
					elif event.text.upper() == "Уведомлять Mid, Mid, Mid".upper():
						print("Уведомлять Mid, Mid, Mid")
					elif event.text.upper() == "Включить все уведомления".upper():
						print("Включить все уведомления")
					elif event.text.upper() == "Не уведомлять Mid, Mid, Mid".upper():
						print("Не уведомлять Mid, Mid, Mid")
					elif event.text.upper() == "Выключить все уведомления".upper():
						print("Выключить все уведомления")
					elif event.text.upper() == "Ссылка Mid".upper():
						print("Ссылка Mid")

					else:
						print('Может попробуешь "Справка"?')
					# print(event.text,event.user_id,event.to_me)




	def send(self,message,person):
		self.vk.method('messages.send', {'user_id':user_id, 'message': message,'random_id':random.randint(1,1000000)})
	def run(self):
		self.handler()
		

VkNotify(c.token).run()