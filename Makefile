
# где установлен питон и какая ос
PYTHON:=$(shell which python3) 
OS := $(shell uname)

# 
help: 
	@echo "путь до python3: ${PYTHON}" 
	@echo "make run - запуск приложения + запуск БД" 
	@echo "make stop - остановка БД" 
	@echo "make installPyReq - установка зависимостей для python3" 
	@echo "make installMysql - установка mysql" 

# установка зависимостей
installPyReq:
	pip3 install -r src/requirements.txt

# macOS
ifeq ($(OS), Darwin)
run: 
	brew services start mysql
	@$(PYTHON) src/main.py
stop: 
	brew services stop mysql
installMysql:
	brew install mysql
endif

# linux
ifeq ($(OS),Linux)
run: 
	sudo systemctl start mysql.service
	@$(PYTHON) src/main.py
stop: 
	sudo systemctl stop mysql.service
installMysql:
	sudo apt install mysql-server
# sudo mysql
# -- for MySQL
# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
# -- for MariaDB
# ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('');
endif

