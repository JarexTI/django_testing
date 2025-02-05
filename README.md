# Тестирование проектов YaNote и YaNews (RU)

Описание проекта
---
В проект были написаны тесты для приложений YaNote (сервис для создания заметок) и YaNews (сервис для просмотра новостей). В нем реализованы ключевые тесты для маршрутов, доступа к страницам, создания и редактирования записей и комментариев, а также работы с пользователями и авторизацией. Для ya_news - pytest; ya_note - unittest.

Основные задачи
---
✔️ Написание тестов для маршрутов и доступности страниц  
✔️ Реализация тестов для создания и редактирования заметок и комментариев  
✔️ Проверка логики работы с пользователями и правами доступа

Стек технологий
---
- Python 3.9
- Django 3.2
- unittest
- pytest

Установка проекта из репозитория (Windows)
---
1. Клонировать репозиторий:
```bash
git clone git@github.com:JarexTI/django_testing.git
```
2. Создать и активировать виртуальное окружение:
```bash
python -m venv venv

source venv/Scripts/activate
```
3. Установить зависимости из файла `requirements.txt`:
```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```
4. Выполнить миграции
```
python ya_news/manage.py migrate

python ya_note/manage.py migrate
```
5. Запустить проект:
```bash
bash run_tests.sh
```
<br>

# Testing of YaNote and YaNews Projects (EN)

Project Description
---
This project contains tests for the YaNote (note-taking service) and YaNews (news viewing service) applications. Key tests have been implemented for routes, page access, creation and editing of posts and comments, as well as user management and authorization. For ya_news - pytest; ya_note - unittest.

Main Tasks
---
✔️ Writing tests for routes and page accessibility  
✔️ Implementing tests for creating and editing notes and comments  
✔️ Checking the logic of user handling and access rights

Tech Stack
---
- Python 3.9
- Django 3.2
- unittest
- pytest

Project Setup from Repository (Windows)
---
1. Clone the repository:

```bash
git clone git@github.com:JarexTI/django_testing.git
```

2. Create and activate a virtual environment:

```bash
python -m venv venv

source venv/Scripts/activate
```

3. Install dependencies from the `requirements.txt` file:

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

4. Run migrations:

```
python ya_news/manage.py migrate

python ya_note/manage.py migrate
```

5. Run the tests:

```bash
bash run_tests.sh
```
