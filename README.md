# Bewise.ai test task
Простой веб-интерфейс для получения вопросов для викторины. 

# Стек:
* Python 3.11
* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker/Docker-compose

# Функционал:
* Получение указанного кол-ва уникальных вопросов со стороннего API
* Сохранение полученных вопросов в БД
* Возврат массива сохраненных в БД вопросов (пустой массив, если сохраненные вопросы отсутствуют)
* Не рекомендуется запрашивать более ~1000 вопросов/раз. \
Из-за ограничений стороннего API на количество операций/ед. времени выполнение запроса займет много времени.
* И самое главное: You aren`t gonna need it - ничего лишнего

# Инструкция по локальному запуску проекта:
* `git clone https://github.com/querdy/bewise_test_task.git`
* `cd bewise_test_task`
* Переименовать файл .env_example в .env и заполнить его необходимыми данными (можно использовать имеющиеся и ограничиться переименованием)
* `docker-compose up -d --build` - запуск приложения

# Документация к API доступна по адресу:
```
http://127.0.0.1:8000/api/docs
```
# Пример запроса:
Request:
```
POST http://127.0.0.1:8000/api/question/
    body: {"questions_num": 1}
```
Response:
```
[
  {
    "question_id": 200408,
    "text": "This conifer known for its durable timber is represented on the flag of Lebanon",
    "answer": "the cedar",
    "created_at": "2022-12-30T21:45:43.803000Z",
    "uuid": "c55bb5aa-15ab-472b-962c-a23f2fb96852"
  }
]
```
