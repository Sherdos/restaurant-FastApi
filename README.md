# Restaurant-FastAPI

[![python](https://img.shields.io/badge/python-3.10_slim-blue?style=flat-square)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.100.0-critical?style=flat-square)](https://fastapi.tiangolo.com/)
[![pytest](https://img.shields.io/badge/pytest-passed-brightgreen)](https://docs.pytest.org/en/7.4.x/)


## Описание

Образовательный проект FastAPI для Y_Lab. Это серверная служба для ресторанов с операциями меню CRUD. Есть три сущности: Меню, Подменю, Блюда.
Документацию можно найти по адресу (http://0.0.0.0:8000/docs,
http://localhost:8000/docs или http://127.0.0.1:8000/docs)

## Выполненные задачи с звездами

### Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
путь к нему src/menu/repositories.py строка 18:24

### Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest
путь к нему test/test_count.py

## Настройка проекта

### Для запуска проекта

1) Соберите docker-compose командой "docker-compose -f docker-compose.yml build"
2) Запустите docker-compose командой "docker-compose -f docker-compose.yml up" добавите " -d " для скрытия дебуга
3) Перейдите по этой ссылке "http://127.0.0.1:8000/"

Все готово

## Для запуска Тестов

1) Соберите docker-compose командой "docker-compose -f docker-compose-test.yml build"
2) Запустите docker-compose командой "docker-compose -f docker-compose-test.yml up"

В консоли покажутся результаты тестов чтобы выйти нажмите на 'Ctrl + C'

## Как работает админ панел

### Внесении изменении в файл
Изменение нужно подверждать знаком в 'H' таблице
1) Для добавление. После добавление всех полей нужно прописать 'C'
2) Для обновление. После внесении всех изменений нужно прописать 'U'
3) Для удаление. Нужно прописать 'D', но удалятся и все связанные объекты
