# //
# //    Mezuzah - поисковой парсер
# //
# //  Created by 
# //    Соколов Борух ККСО-04-21
# //    Кузьмин Данил ККСО-04-21


# user="wedlec" 
# password="root"

# настройка mysql
host="localhost" 
# пользователь для работы с БД (по умолчанию)
user="root" 
password=""
database="mezuzah"        # DROP DATABASE mezuzah 
#

# библиотеки для работы с GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# подключение своих методов
from ip import *        # описаны ф-я по получению ip + mac
from sql import *       # описан класс для работы с БД

# библиотеки для работы с запросами и парсингом
import requests                       # ползваляет удобно делать запросы
from bs4 import BeautifulSoup         # ползваляет удобно парсить html документ (get запрос от requests)
from urllib.parse import urlparse     # позволяет удобно пасить URL

# библиотеки для работы с потоками и временем
import threading    # позволяет удобно работать с потоками
import time         # позволяет удобно работать с временем

# выполнение поиска статей в другом потоке
def perform_search():
    threading.Thread(target=search_articles).start()   
# поиск статей
def search_articles():
    try:
        keywords = entry.get()  # Получаем ключевые слова из поля ввода
        search_time = int(entry_time.get())  # Получаем время поиска в секундах

    except Exception as e:
        messagebox.showerror("Ошибка 404:", f"Произошла ошибка: \nвведите ключевое слово и укажите время ({e})")
       
    
    # Очищаем таблицу перед новым запросом
    tree.delete(*tree.get_children())

    # Собираем результаты с сайтами, заголовками и ссылками
    top_results = []
    start_time = time.time()
    current_id = 1  # Уникальный ID для таблицы

    # работаем по указаному времени
    while time.time() - start_time < search_time:
        # указываем поисковой запрос (и если надо то перематываем страницы поиска(где начать))
        url = f"https://www.google.com/search?q={'+'.join(keywords.split())}&start={len(top_results)}"
        # указываем юзер агент
        headers = {'User-Agent': 'Mozilla/4.0'}
        # получаем ответ ссылок
        response = requests.get(url, headers=headers)
        time.sleep(1)  # Задержка между запросами по страницам

        # если есть ответ 'успешно' 
        if response.status_code == 200:
            # парсим ответ 
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')  # Получаем все ссылки на странице

            # проходимся по всем ссылкам
            for link in links:
                href = link.get('href') 
                
                if href.startswith('/url?q='):  # Проверяем, что это ссылка на результаты поиска Google
                    
                    # при получении ссылки из поисковой выдачи Google, 
                    # она содержит дополнительные параметры '/url?q=' и '&' 
                    # которые не нужны нам для дальнейшей работы со ссылкой.

                    # удаляем эти параметры разделяя на '/url?q=' и удаляем всё что идёт после '&'
                    clean_link = href.split('/url?q=')[1].split('&')[0]

                    title = link.text  # Заголовок статьи
                    # разбирает URL на его компоненты 
                    parsed_uri = urlparse(clean_link) #url = "https://www.example.com/path? print(urlparse(url).netloc) => 'www.example.com'
                    # форматируем строку в домен
                    domain = '{uri.netloc}'.format(uri=parsed_uri) 

                    # добавим в наш список
                    top_results.append((current_id, domain, title, clean_link))
                    current_id += 1

            # Обновляем прогресс поиска
            current_time = time.time() - start_time
            search_percentage = min((current_time / search_time) * 100, 100)

            label_progress.config(text=f"Процент выполнения: {search_percentage:.1f}%")
            label_time_left.config(text=f"Осталось времени: {search_time - current_time:.1f} сек")
        
    # Отображаем результаты поиска в таблицу
    for item in top_results:
        tree.insert("", tk.END, values=(f"{item[0]}", item[1], item[2], item[3])) 
    label_progress.config(text=f"Процент выполнения: 100%")
    label_time_left.config(text="Поиск завершён")

# выполнение отправка статей в БД в другом потоке
def perform_insert_results_to_db():
    threading.Thread(target=insert_results_to_db).start()   
# отправка статей в БД
def insert_results_to_db():

    try:

        # Создаем объект класса DatabaseConnector
        db_connector = DatabaseConnector(host=host, user=user, password=password, database=database)
        # подключаемся к БД
        db_connector.connect() 

        # создание таблицы webpage (если она есть то ок)
        create_table_query = "CREATE TABLE IF NOT EXISTS webpage (id INT AUTO_INCREMENT PRIMARY KEY, site VARCHAR(255), title VARCHAR(255),href VARCHAR(255) )"
        # выполняем команду создания таб
        db_connector.execute_query(create_table_query)
        
        
        # Получаем все элементы из таблицы
        items = tree.get_children()
        for item in items:
            values = tree.item(item, 'values')
            id, domain, title, href = values
            # отправляем значения
            db_connector.insert_webpage(domain, title, href)

        messagebox.showinfo("Успешно", "добавлено в таблицу")

        # Выбираем и выводим в консоль данные из таблицы webPage
        select_query = "SELECT * FROM webPage"
        result = db_connector.fetch_all(select_query)
        if result:
            for row in result:
                print(row)

        # Закрываем соединение с базой данных
        db_connector.disconnect()
    except:
         messagebox.showinfo("Ошибка", "Ошибка в подключении к БД mysql.\n Включите mysql!")

#  UI создание кнопок действия
def create_search_interface(root):
    label = tk.Label(root, text="Введите ключевые слова:")
    label.pack()

    global entry, entry_time
    entry = tk.Entry(root, width=50)
    entry.pack()

    label_time = tk.Label(root, text="Время поиска (сек):")
    label_time.pack()

    entry_time = tk.Entry(root)
    entry_time.pack()

    # соверщаем поиск в другом потоке 
    button_search = tk.Button(root, text="Поиск", command=perform_search)
    button_search.pack()
# UI создание таблицы
def create_results_table(root):
    global tree
    tree = ttk.Treeview(root, columns=("id", "site", "title", "href"), show="headings")
    tree.pack(fill="both", expand=True)
    tree.heading("id", text="id", anchor=tk.CENTER)
    tree.heading("site", text="site", anchor=tk.CENTER)
    tree.heading("title", text="title", anchor=tk.CENTER)
    tree.heading("href", text="href", anchor=tk.CENTER)

    tree.column("#1", width=20, anchor=tk.CENTER)
    tree.column("#2", width=150, anchor=tk.CENTER)
    tree.column("#3", width=250, anchor=tk.CENTER)
    tree.column("#4", width=300, anchor=tk.CENTER)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
# UI создание инфы от ip и % выполнения 
def create_progress_labels(root):
    label_local_ip = tk.Label(root, text=f"Local IP: {get_local_ip()}")
    label_local_ip.pack(side=tk.BOTTOM, anchor=tk.SW)

    label_public_ip = tk.Label(root, text=f"Public IP: {get_public_ip()}")
    label_public_ip.pack()
    label_public_ip.pack(side=tk.BOTTOM, anchor=tk.SW)

    label_mac_address = tk.Label(root, text=f"MAC Address: {get_mac_address()}")
    label_mac_address.pack()
    label_mac_address.pack(side=tk.BOTTOM, anchor=tk.SW)

    global label_progress, label_time_left
    label_progress = tk.Label(root, text="Процент выполнения: 0%")
    label_progress.pack()

    label_time_left = tk.Label(root, text="Осталось времени: 0 сек")
    label_time_left.pack()


def main():
    # создаёи окно GUI приложения
    root = tk.Tk()
    root.title("Мезуза")

    # GUI приложения
    create_search_interface(root)
    create_results_table(root)
    create_progress_labels(root)

    # GUI кнопка отправки статей в БД
    button_save_to_db = tk.Button(root, text="Сохранить в БД", command=perform_insert_results_to_db)
    button_save_to_db.pack()

    # зацикливаем приложение
    root.mainloop()

if __name__ == '__main__':
    main()