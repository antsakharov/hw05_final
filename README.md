# yatube_project

## Описание проекта: 

•	**Назначение:** 

Финальная версия социальной сети для публикации личных дневников. 

•	**Реализованный функционал:** 

1. Созданы кастомные страницы для ошибок
2. Написан тест, проверяющий, что страница 404 отдаёт кастомный шаблон
3. Добавлена система подписки на авторов
4. Создана лента постов авторов
5. Написаны тесты, проверяющие работу нового сервиса

•	**Цель выполнения проекта:**

Практика использования Unittest

•	**Стек:**

Python 3.7, Django 2.2.19, SQLite, pytest, Unittest.

## Инструкция по развёртыванию проекта

•	**Клонируйте репозиторий:**

```csharp 
git clone git@github.com:antsakharov/hw05_final.git
```

•	**Установите и активируйте виртуальное окружение:**

**для Linux и MacOS**

```csharp 
python3 -m venv venv
```

**для Windows**

```csharp 
python -m venv venv
```

```csharp 
source venv/bin/activate
```

```csharp 
source venv/Scripts/activate
```

•	**Установите зависимости из файла requirements.txt:**

```csharp 
pip install -r requirements.txt
```
•	**Создайте и выполните миграции:**

```csharp 
python manage.py makemigrations
```

```csharp 
python manage.py migrate
```

