# //
# //    Mezuzah - поисковой парсер
# //
# //  Created by 
# //    Соколов Борух ККСО-04-21
# //    Кузьмин Данил ККСО-04-21

# файл ip.py описывает ф-я получения ip + mac


import netifaces # библиотека для получения сетевых интерфейсов
import requests  # библиотека для отправки запростов 

def get_local_ip():
    try:
        local_ip = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']
        return local_ip
    except:
        return "N/A"
    
def get_public_ip():
    try:
        # api получения публичного ip
        response = requests.get('https://api.ipify.org').text
        return response
    except requests.RequestException as e:
        print(f"Ошибка получения публичного IP: {e}")
        return "N/A"


def get_mac_address():
    try:
        mac_address = netifaces.ifaddresses('en0')[netifaces.AF_LINK][0]['addr']
        return mac_address
    except:
        return "N/A"