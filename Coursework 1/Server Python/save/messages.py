from data_person import DataPerson
from data_item import DataItem

class Message(): # 12 сообщений
	def __init__(self,user_id,Type):
		self.type = Type
		self.user_id=user_id

		# Должен возвращать текст в зависимости от команды
	def handler_(self):
		if self.type ==0: # Справка
			return "Доступные команды:\n\
					- Отслеживаемое\n\
					- Добавить /link\n\
					- Добавить Mid\n\
					- Удалить /link\n\
					- Удалить Mid\n\
					- Удалить все\n\
					- Уведомлять Mid, Mid, Mid\n\
					- Не уведомлять Mid, Mid, Mid\n\
					- Включить все уведомления\n\
					- Выключить все уведомления\n\
					- Ссылка Mid\n\
					- Справка\n "
		elif self.type ==1: # Отслеживаемое, 
			tracked_string = ""
			login = DataPerson().get_login_from_VkUser_id(self.user_id)
			tracked_items = DataPerson().get_tracked(login)
			for element in tracked_items:
				data = DataItem().get(element)
				tracked_string.join(str(data["Mid"]+" "+data["name"]+"/"+data["brand"]+"\t"+data["price"]+"\n"))
			print(tracked_string)
			for el in tracked_string:
				
			return tracked_string
			# В таблице настроек ищет привязанный логин к иду
			# с логином достает Mid айтемов которые отслеживаются
			# Применяется класс data, далее составляю текст
