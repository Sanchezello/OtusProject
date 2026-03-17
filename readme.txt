Настройка и развёртывание:

Python
Windows: https://www.python.org/downloads/ 

Git
https://git-scm.com/download
git config --global user.name ""
git config --global user.email ""

Установка JDK для Jenkins и allure
Переменные среды пользователя - Создать
Имя: JAVA_HOME
Значение: C:\Program Files\...
PATH добавить:
%JAVA_HOME%\bin


Allure
https://github.com/allure-framework/allure2/releases
C:\allure
В PATH: C:\allure\bin

java -version
echo $env:JAVA_HOME


docker compose up -d

Магазин: http://localhost:8081
pub@prestashop.com
1qaz@WSX3edc	- поменять в админке

Админка: http://localhost:8081/administration
Логин: admin@example.com
Пароль: Admin123!

Создать ключ, заменить в конфиге
Если вручную не запускаем тесты, то меняем хост в админке

БД: http://localhost:8888
Логин: root
Пароль: admin

Jenkins
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword


Plugins:
Allure
Git				
Pipeline
Credentials     для доступа к гиту по токену
Matrix          важная шляпа для Allure plugin




pip install --upgrade pip
pip install -r requirements.txt



Manual tests:

py -m pytest tests/ui/test_home_page.py -v --alluredir=./allure-results
allure serve ./allure-results



/////////////////////////////////////////////////////////////////////////////////////////


1) Создали токен, добавили в ридми. (для проверки работы, знаю что так нельзя.)
2)Изменили настройки на локальные. config.py
3) запустили докер из директории проекта docker-compose up -d
4) проверяем 8888 - БД престы
5)проверяем  8081 --->>> docker-compose restart prestashop (Если не стартанул преста)
6)http://localhost:8081/administration        ADMIN_MAIL: admin@example.com # Данные для входа в админку
      ADMIN_PASSWD: Admin123!
7) Запускаем вебсервис, создаем API-key,заменяем в config.py Выдаем пермишены на Кей в админке
8)ДЛя кастомера J.DOE Меняем пасс на 1qaz@WSX3edc http://localhost:8081/administration/sell/customers/
9) меняем хост на prestashop http://localhost:8081/administration/configure/shop/seo-urls/
10)Меняем конфиги на престу в config.py , Пушим изменения. 
11) Идем в Jenkins http://localhost:8080/manage/pluginManager/, ставим плагины:

	Plugins:
	Allure
	Git				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      github-token
	Pipeline
	Credentials     для доступа к гиту по токену
	Matrix          важная шляпа для Allure plugin
12) Идем http://localhost:8080/manage/configureTools/
	Добавляем Allurecomanline
	ВАЖНО: Версия 2.36
	
13) http://localhost:8080/manage/credentials/store/system/domain/_/ Настраиваем креды.
	System-global-Add Credentials Type:"Username, password"
	Авторизация по гитовой учетке, с использованием сгенерированного токена. где:
		password - токен
		id -"github-token"
		
14) Идем в Jenkins, создаем итем http://localhost:8080/ создаем пайплайн:
	Definition: Pipeline sript from SCM
	SCM- Git
	URL- Ссыль на урл (https://github.com/Sanchezello/ProjectGodzilla.git)
	Креды из ш.13, выпадающий список
15) идем и запускаем пайплайн
	
