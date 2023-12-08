
# где установлен питон и какая ос
PYTHON:=$(shell which python3) 
OS := $(shell uname)

# 
help: 
	@echo "путь до python3: ${PYTHON}" 
	@echo "make help - помощь по запуску" 
	@echo "make run - запуск приложения" 
	@echo "make startDB - запуск БД mysql" 
	@echo "make stopDB - остановка БД mysql" 
	@echo "make installPyReq - установка зависимостей для python3" 
	@echo "make installMysql - установка mysql" 
	@echo "make conficMysql - установка конфига для mysql (только linux)" 

run: 
	@$(PYTHON) src/main.py

# установка зависимостей
installPyReq:
	pip3 install -r src/requirements.txt

# macOS
ifeq ($(OS), Darwin)
startDB: 
	brew services start mysql
stopDB: 
	brew services stop mysql
installMysql:
	brew install mysql
endif

# linux
ifeq ($(OS),Linux)
startDB: 
	sudo systemctl start mysql.service
stopDB: 
	sudo systemctl stop mysql.service
installMysql:
	sudo apt install mysql-server
	conficMysql
conficMysql:
	@echo "введите команду:'ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('');' " 
	sudo mysql
# в linux mysql нужно явно указать пароль для root
# 1) sudo mysql
# 2) use mezuzah
# 3)SELECT * FROM `webpage` WHERE 1;
# DROP DATABASE mezuzah 
endif

