# //
# //    Mezuzah - поисковой парсер
# //
# //  Created by 
# //    Соколов Борух ККСО-04-21
# //    Кузьмин Данил ККСО-04-21

# файл sql.py описывает класс для работы с БД
# вся настройка по подключнию mysql описана в файле main.py

import mysql.connector

# создаём класс для удбной работы с БД
class DatabaseConnector:
    # конструктор (инициализация переменных и создание БД)
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

        # создаём бд 
        try:
            #  Устанавливаем соединение с MySQL
            self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password)
                            
            # Создаем объект cursor для выполнения SQL-запросов
            self.cursor = self.connection.cursor()
            # Создаем базу данных 'mezuzah', если она еще не существует
            cretDB = f"CREATE DATABASE IF NOT EXISTS {self.database}"
            self.cursor.execute(cretDB)
            # Закрываем соединение с MySQL
            self.cursor.close()
            self.connection.close()
        except mysql.connector.Error as err:
            print(f"Произошла ошибка при создании базы данных: {err}")
            print(f"Проверьте включен ли mysql")



        

    # ф-я подключения к БД
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Подключено к базе данных")
        except mysql.connector.Error as err:
            print("Ошибка подключения 401:", err)

    # ф-я отключения от БД
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Отключено от базы данных")

    # Функция execute_query выполняет переданный SQL-запрос. 
    # Она используется для операций которые изменяют данные в базе данных
    # таких как создание таблицы (`CREATE TABLE`), вставка новых записей (`INSERT INTO`), 
    # обновление или удаление записей (`UPDATE`, DELETE`). 
    # Эта функция возвращает `True, если запрос успешно выполнен, и False в случае ошибки.
    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print("Ошибка выполнения запроса 402:", err)
            return False
    

    # Функция fetch_all используется для выборки данных из базы данных. 
    # Она выполняет SQL-запрос и получает все строки, соответствующие запросу. 
    # Возвращает результат выборки в виде списка кортежей!, где каждый кортеж представляет 
    # собой строку данных из результата запроса. Эти данные могут быть обработаны или 
    # выведены в консоль
    def fetch_all(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print("Ошибка выполнения запроса 403:", err)
            return None
        
    # ф-я вставки данных в таблицу webpage
    def insert_webpage(self, site, title, href):
        #вставка данных в таблицу webpage
        insert_query = "INSERT INTO webpage (site, title, href) VALUES (%s, %s, %s)"
        insert_params = (site, title, href)
        return self.execute_query(insert_query, insert_params)
  