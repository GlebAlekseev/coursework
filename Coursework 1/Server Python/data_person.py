import sqlite3
class DataPerson():
	def __init__(self):
		pass
	def get_login_from_VkUser_id(self,user_id):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		#Итак, еще одна таблица users_settings отвечает за настройки каждого пользовател
		try:
			cursor.execute("""CREATE TABLE users_settings
				(login text, pages text,style text,link_vk text,key_ text)
				""")
		except sqlite3.OperationalError:
			# print("БД уже создана")
			pass
		else:
			# print("Создание БД")
			pass

		cursor.execute('SELECT * FROM users_settings WHERE link_vk=?', (user_id, ))
		settings = cursor.fetchone()
		if settings is None:
			connect.commit()
			connect.close()	
			return None
		else:
			cursor.execute('SELECT * FROM users_settings WHERE link_vk=?', (user_id, ))
			data = cursor.fetchone()
			for element in data:
				connect.commit()
				connect.close()	
				return element[0]
	def insert_Mid(self,login,Mid):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid =?' , (login,Mid,))
		if info.fetchone() is None:
			
			#insert
			cursor.execute("INSERT INTO user_tracking  (login,Mid,tracking)VALUES (?,?,?)", (login,Mid,0))
			connect.commit()
			connect.close()	
			return "220"
		else:
			connect.commit()
			connect.close()	
			return "221"
			# уже есть

	def get_tracked(self,login):
		trd_items = []
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
		info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid =?' , (login,1,))
		tracked_items = info.fetchall()
		for element in tracked_items:
			trd_items.append(element[1])
		connect.commit()
		connect.close()	
		return trd_items

	def get_tracking_status(self,login,Mid):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()	

		info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid =?' , (login,Mid,))
		if info.fetchone() is None:
			connect.commit()
			connect.close()	
			return "9010"


		info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid =?' , (login,Mid,))
		data = info.fetchall()
		status = 0
		for element in data:
			status = element[3]
			break
		# аа что если товара нет в отслежке


		connect.close()	
		return status


	
	def set_tracking_status(self,login,Mid,bool_):

		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		info = cursor.execute('SELECT * FROM user_tracking WHERE login=? AND Mid =?' , (login,Mid,))
		if info.fetchone() is None:
			connect.commit()
			connect.close()	
			return "901"


		cursor.execute('UPDATE user_tracking SET tracking = ? WHERE login = ? AND Mid = ?',(bool_,login,Mid,))

		connect.commit()
		connect.close()	
		return "900"



	def get(self,login):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		#Итак, еще одна таблица users_settings отвечает за настройки каждого пользовател
		try:
			cursor.execute("""CREATE TABLE users_settings
				(login text, pages text,style text,link_vk text,key_ text)
				""")
		except sqlite3.OperationalError:
			# print("БД уже создана")
			pass
		else:
			# print("Создание БД")
			pass

		cursor.execute('SELECT * FROM users_settings WHERE login=?', (login, ))
		settings = cursor.fetchone()
		if settings is None:
			self.set(login)
			# Нету настроек
			# Внос стандарта
			

		cursor.execute('SELECT * FROM users_settings WHERE login=?', (login, ))
		data = cursor.fetchall()
		for element in data:
			connect.commit()
			connect.close()	
			return (element[0],element[1],element[2],element[3],element[4])
			

		# Получает данные из таблицы

	def set(self,login,pages = 10,style=";;",link_vk=None):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()

		try:
			cursor.execute("""CREATE TABLE users_settings
				(login text, pages text,style text,link_vk text,key_ text)
				""")
		except sqlite3.OperationalError:
			# print("БД уже создана")
			pass
		else:
			# print("Создание БД")
			pass

		cursor.execute('SELECT * FROM users_settings WHERE login=?', (login, ))
		if cursor.fetchone() is None: # Если отсутствует
			cursor.execute("INSERT INTO users_settings  (login,pages,style,link_vk)VALUES (?,?,?,?)", (login,pages,style,link_vk,))
		else:
			cursor.execute('UPDATE users_settings SET pages= ?,style = ?,link_vk = ? WHERE login = ?',(pages,style,link_vk,login,))
		connect.commit()
		connect.close()	
	def edit(self,login,pages = None,style=None,link_vk=None,key_=None):
		connect = sqlite3.connect("data.db") 
		connect.isolation_level= 'DEFERRED'
		cursor = connect.cursor()
		try:
			cursor.execute("""CREATE TABLE users_settings
				(login text, pages text,style text,link_vk text,key_ text)
				""")
		except sqlite3.OperationalError:
			# print("БД уже создана")
			pass
		else:
			# print("Создание БД")
			pass
		cursor.execute('SELECT * FROM users_settings WHERE login=?', (login, ))
		if cursor.fetchone() is None: # Если отсутствует
			connect.commit()
			connect.close()	
			return
		else:
			if pages != None:
				cursor.execute('UPDATE users_settings SET pages= ? WHERE login = ?',(pages,login,))
			if style != None:
				cursor.execute('UPDATE users_settings SET style = ? WHERE login = ?',(style,login,))
			if link_vk != None:
				cursor.execute('UPDATE users_settings SET link_vk = ? WHERE login = ?',(link_vk,login,))
			if key_ != None:
				cursor.execute('UPDATE users_settings SET key_ = ? WHERE login = ?',(key_,login,))

			connect.commit()
			connect.close()	