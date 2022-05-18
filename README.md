<h1 align="center"> Pulic Notes </h1>

<p align="center">
  <a href="https://github.com/Yu-Leo/public-notes/blob/main/LICENSE" target="_blank"> <img alt="license" src="https://img.shields.io/github/license/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/public-notes/releases/latest" target="_blank"> <img alt="last release" src="https://img.shields.io/github/v/release/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/public-notes/commits/main" target="_blank"> <img alt="last commit" src="https://img.shields.io/github/last-commit/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/public-notes/graphs/contributors" target="_blank"> <img alt="commit activity" src="https://img.shields.io/github/commit-activity/m/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
</p>

## Навигация

* [Описание проекта](#chapter-0)
* [Как начать](#chapter-1)
* [Интерфейс](#chapter-2)
* [Код](#chapter-3)
* [Лицензия](#chapter-5)

<a id="chapter-0"></a>

## :page_facing_up: Описание проекта

Простой сайт на **Django**. Пользователи могут оставлять заметки, которые будут видны всем на главной странице сайта.

<a id="chapter-1"></a>

## :hammer: Как начать

Инструкция по установке, быстрой настройке и запуску проекта.

1. Скачать данный репозиторий
    * Вариант 1
        1. Установить [Git](https://git-scm.com/download/win)
        2. Клонировать репозиторий
       ```bash
       git clone https://github.com/Yu-Leo/public-notes.git
       cd public-notes
       ```
    * Вариант 2 - [Скачать ZIP](https://github.com/Yu-Leo/public-notes/archive/refs/heads/main.zip)
2. Создать виртуальное окружение
    ```bash
    python3 -m venv venv
    ```
3. Активировать виртуальное окружение
    ```bash
    source venv/bin/activate
    ```
4. Установить зависимости проекта
    ```bash
    pip install -r requirements.txt
    ```
5. Запустить сервер
    ```bash
    cd publicnotes
    python manage.py runserver
    ```

<a id="chapter-2"></a>

## :camera: Интерфейс

- **Главная** - главная страница сайта, на которой отображаются все заметки.
- **О проекте** - страница с информацией о проекте
- **Категории** - распределение заметок по категориям
- **Авторы** - список авторов, оставивших свои заметки на сайте
- **Добавить категорию** - отобрадение списка существующих категорий и возможность добавить свою (только для
  авторизованных пользователей)
- **Добавить заметку** - форма добавления заметки (только для авторизованных пользователей)
- **\<username\>** - профиль пользователя (только для авторизованных пользователей)

<a id="chapter-3"></a>

## :computer: Код

[Техническая документация]() (в `./docs/technical-documentation.pdf`)

### :wrench: Используемые технологии

#### BackEnd:

- Язык программирования: **Python (3.10)**
- Фреймворки и библиотеки:
    - **Django (3.0.2)**
    - **django_debug_toolbar (2.2)**

#### FrontEnd:

- Языки: **html**, **css**
- Фреймворки и библиотеки:
    - **Bootstrap 5**

### :file_folder: Папки

- **publicnotes** - исходный код проекта
    - **media** - папка с медиа-изображениями
    - **publicnotes** - настройки проекта
    - **templates** - общие шаблоны проекта
    - **wall** - главное приложение
        - **migragions** - файлы миграций
        - **static** - файлы статики
        - **templates** - шаблоны приложения
        - **templatetags** - самописные теги
- **docs** - документация

<a id="chapter-5"></a>

## :open_hands: Лицензия

Используете мой код - ставьте звёздочку ⭐️ на репозиторий

Автор: [Yu-Leo](https://github.com/Yu-Leo)

GNU General Public License v3.0

Полный текст в [LICENSE](LICENSE)
