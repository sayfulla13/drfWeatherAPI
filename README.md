## 🚀 Функционал  
✅ Регистрация и авторизация пользователей (по сессиям)  
✅ Разделение ролей (**user** и **manager**)  
✅ Менеджеры могут добавлять города  
✅ Автоматическое обновление погоды, если данные старше 10 минут  

Клон репозитория и установка зависимостей :
1)git clone https://github.com/sayfulla13/drfWeatherAPI.git


2)cd drfWeatherAPI



3)pip install django djangorestframework requests


4)python manage.py makemigrations



5)python manage.py migrate



6)python manage.py runserver




Регистрация :
POST http://127.0.0.1:8000/register/ 
Body :
1)для юзера
{
    "username":"user1",
    "password":"password1",
    "email":"mail1@gmail.com",
    "status":"user",
    "city":"Almaty"
}
2)для менеджера
{
    "username":"user2",
    "password":"password2",
    "email":"mail2@gmail.com",
    "status":"manager"
}

ОТВЕТ : 
{
    "message": "Пользователь зарегистрирован"
}

Вход :

POST http://127.0.0.1:8000/login/
Body :
{
    "username":"user2",
    "password":"password2"
}

ОТВЕТ :
{
    "message": "Вход выполнен",
    "user": {
        "id": 2,
        "username": "user2",
        "email": "mail2@gmail.com",
        "status": "manager",
        "city": null
    }
}

###ПРИМИЧАНИЕ : для некоторых POST запросов необходимо добавить CSRF токен в ЗАГОЛОВКИ(CSRF токен можно взять с кук )
{
    "X-CSRFToken": "your_csrf_token"
}
Выход с аккаунта :
POST http://127.0.0.1:8000/logout/
ОТВЕТ : 
{
    "message": "Вы вышли из системы"
}

Просмотр погоды (только для юзеров):
GET http://127.0.0.1:8000/weather/

ОТВЕТ :

{
    "city": "Almaty",
    "temp": -0.05,
    "description": "smoke",
    "last_update": "2025-02-20T06:43:42.239869Z"
}

Добавление городов (только для менеджеров):
 POST http://127.0.0.1:8000/addcity/

 Body :
{
    "city":"Moscow"
}

ОТВЕТ :
{
    "message": "Город добавлен",
    "data": {
        "city": "Moscow",
        "temp": -6.86,
        "description": "scattered clouds",
        "last_update": "2025-02-20T06:47:18.861454Z"
    }
}
