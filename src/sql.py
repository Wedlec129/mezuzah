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
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

        # создаём бд (если БД есть то ничего сташного ;) )
        try:
            #  Устанавливаем соединение с MySQL
            connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password)
                            
            # Создаем объект cursor для выполнения SQL-запросов
            cursor = connection.cursor()
            # Создаем базу данных 'mezuzah', если она еще не существует
            cretDB = f"CREATE DATABASE IF NOT EXISTS {self.database}"
            cursor.execute(cretDB)
            # Закрываем соединение с MySQL
            cursor.close()
            connection.close()
        except:
            print(f"Произошла ошибка при создании базы данных: {e}")

        finally:
            try:

                # подключаемся к БД
                db_connector = DatabaseConnector(host=self.host, user=self.user, password=self.password)
                db_connector.connect()

                create_database_query = f"CREATE DATABASE IF NOT EXISTS {self.database}"
                db_connector.execute_query(create_database_query)

                db_connector.disconnect()
            except Exception as e:
                print(f"Произошла ошибка при создании базы данных: {e}")
        

    # ф-я подключения к БД
    def connect(self):
        try:
            
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Подключено к базе данных")
        except mysql.connector.Error as err:
            print("Ошибка подключения:", err)

    # ф-я отключения от БД
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Отключено от базы данных")

    # Функция execute_query в классе для работы с базой данных выполняет переданный SQL-запрос. 
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
            print("Ошибка выполнения запроса:", err)
            return False
    

    # Функция fetch_all используется для выборки данных из базы данных. 
    # Она выполняет SQL-запрос и получает все строки, соответствующие запросу. 
    # Возвращает результат выборки в виде списка кортежей, где каждый кортеж представляет 
    # собой строку данных из результата запроса. Эти данные могут быть обработаны или 
    # выведены в консоль, как показано в примере.
    def fetch_all(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print("Ошибка выполнения запроса:", err)
            return None
        
    # ф-я вставки данных в таблицу webpage
    def insert_webpage(self, site, title, href):

        #вставка данных в таблицу webpage
        insert_query = "INSERT INTO webpage (site, title, href) VALUES (%s, %s, %s)"
        insert_params = (site, title, href)
        return self.execute_query(insert_query, insert_params)
    
