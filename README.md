# Laboratory 11
# СОСТАВ КОМАНДЫ: 
504695 Карелина Милана
503294 Мацеюк Артем
504634 Халилов Чингиз

Скринкаст: https://drive.google.com/file/d/17ZqM-48R76B_U8mVDxuB-ir13WZO-5Yo/view?usp=share_link

# Notes App – система управления заметками на Django

## Краткое описание
Веб-приложение для создания и управления заметками. Есть регистрация и вход, поиск по тегам и админ-панель. Проект сделан на Django с использованием Bootstrap 5.

## Быстрый запуск проекта

### 1. Клонирование репозитория
git clone https://github.com/ваш-username/notes-app.git
cd notes-app

### 2. Создание виртуального окружения
python -m venv venv

### 3. Установка зависимостей
pip install django

### 4. Настройка базы данных
python manage.py migrate

### 5. Создание суперпользователя
python manage.py createsuperuser

### 6. Запуск сервера
python manage.py runserver

### 7. Открытие в браузере
Приложение: http://127.0.0.1:8000/
Админка: http://127.0.0.1:8000/admin/

## Архитектура приложения (MTV)
*Model (notes/models.py)*
Note — заметка (заголовок, текст, дата создания и изменения)
Tag — теги для заметок
Profile — расширение пользователя

Связи:
User → Notes (один ко многим)
Notes ↔ Tags (многие ко многим)

*View (notes/views.py)*
Аутентификация: register, user_login, user_logout
CRUD: note_list, note_create, note_detail, note_edit, note_delete

*Template (notes/templates/notes/)*
base.html — базовый шаблон
home.html — главная страница
note_list.html — список заметок
note_form.html — создание и редактирование
login.html, register.html — авторизация

Дополнительные файлы
notes/forms.py — формы
notes/urls.py — маршруты
notes/admin.py — настройка админки
notes_app/settings.py — настройки проекта
notes_app/urls.py — корневая маршрутизация
![sticker](https://github.com/user-attachments/assets/d79b9dbe-a308-4d36-a1fc-fe466b1a3901)



