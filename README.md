<h1 align="center"> Public Notes </h1>

<p align="center">
  <a href="https://github.com/Yu-Leo/public-notes/blob/main/LICENSE" target="_blank"> <img alt="license" src="https://img.shields.io/github/license/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/public-notes/releases/latest" target="_blank"> <img alt="last release" src="https://img.shields.io/github/v/release/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/public-notes/commits/main" target="_blank"> <img alt="last commit" src="https://img.shields.io/github/last-commit/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/public-notes/graphs/contributors" target="_blank"> <img alt="commit activity" src="https://img.shields.io/github/commit-activity/m/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
</p>

<p align="center">
English | <a href="./README_RU.md">Русский</a>
</p>

<hr>

## Navigation

* [Project description](#chapter-0)
* [Interface](#chapter-1)
* [Getting started](#chapter-2)
* [Source code](#chapter-3)
* [License](#chapter-5)

<a id="chapter-0"></a>

## :page_facing_up: Project description

The website where users can write public notes.

### Functionality:

- Notes:
    - Displaying a single list (main page)
    - Displaying by category. Each note can belong to one category
    - Displaying by tags. Each note can have multiple tags
    - Number of views counter
    - Search by titles
    - Adding public and private notes
    - Ability to pin notes (pinned notes will be displayed at the top of the
      list on the profile page)
    - Rating system: each like increases the rating by 1, each dislike decreases
    - Editing
    - Deleting
- Displaying the list of authors
- Profile:
    - Registration
    - Confirmation of e-mail by one-time link
    - Displaying profile and notes
    - Rating system: user's rating is the sum of ratings of his public notes
    - Changing profile data
    - Changing the password
    - Deleting a profile
- Categories:
    - Displaying categories as a list with different levels of nesting
    - Each category can have subcategories. Notes can belong to both parent and
      child categories
- Support for Russian and English languages

<a id="chapter-1"></a>

## :camera: Interface

- **Main** - the main page of the site where all notes are displayed
- **About** - project information page
- **Categories** - distribution of notes by category
- **Categories list** - displaying categories as a list with different levels of
  nesting
- **Authors** - list of authors who wrote notes on the site
- **Add note** - form for adding notes (only for authorized users)
- **Search** - search by note titles
- **\<username\>** - user profile (only for authorized users)

![main_page](./docs/img/main_page.jpg)

![profile_page](./docs/img/profile_page.jpg)

![category_page](./docs/img/category_page.jpg)

<a id="chapter-2"></a>

## :hammer: Getting started

1. Download this repository
    - Option 1
        1. Install [git](https://git-scm.com/download)
        2. Clone this repository
         ```bash
         git clone https://github.com/Yu-Leo/public-notes.git
         cd public-notes
         ```
    - Option 2
      - [Download ZIP](https://github.com/Yu-Leo/public-notes/archive/refs/heads/main.zip)
2. Create `.env` file with [required environment variables](#envvars).
3. Run with docker-compose or configure for development:

### Run using docker-compose:

1. Run:
    ```bash
    docker-compose up --build
    ```
2. Stop:
    ```bash
    docker-compose down
    ```

### Configure for development

1. Create a virtual environment in the project repository
    ```bash
    python3 -m venv venv
    ```
2. Activate the virtual environment
    ```bash
    source venv/bin/activate
    ```
3. Install project dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Compile phrase translations
    1. Install `gettext`:
       ```bash
       sudo apt-get install gettext
       ```
    2. Run in `publicnotes` folder:
       ```bash
          django-admin compilemessages
       ```
5. Run the server
    ```bash
    cd publicnotes
    python manage.py runserver
    ```

<a id="chapter-3"></a>

## :computer: Source code

### :wrench: Technologies

#### BackEnd:

- DBMS: **SQLite3**
- Programming language: **Python (3.10.4)**
- Frameworks and libraries:
    - **Django (3.1.14)**
    - **django_debug_toolbar (2.2.1)**
    - **django_mptt (0.13.4)**
- Web server: **gunicorn**

#### FrontEnd:

- Languages: **html**, **css**
- Frameworks and libraries:
    - **Bootstrap 5**

#### Tools:

- Docker and Docker Compose

### :file_folder: Folders and files

- **publicnotes** - project source code
    - **media** - folder with media files
    - **locale** - folder with translations
    - **config** - project settings
    - **templates** - common project templates
    - **wall** - the main Django application of the project
        - **locale** - folder with translations
        - **migrations** - migration files
        - **services** - business logic of the application
        - **static** - static files
        - **templates** - application templates
        - **templatetags** - custom tags
        - **tests** - tests
        - **admin.py** - admin panel settings
        - **apps.py**
        - **exceptions.py** - custom exceptions
        - **forms.py** - forms and their settings
        - **generate_fake_data.py** - script for generating random notes (for
          manual testing)
        - **models.py** - application models
        - **urls.py** - application URL settings
        - **utils.py** - utilities used in business logic
        - **views.py** - model representations
- **docs** - documentation

### :wrench: Settings

<a id="envvars"></a>

#### Required environment variables:

- `DJANGO_DEBUG` - Run in DEBUG mode or not (set 1 or 0). Default 0.
- `DJANGO_SECRET_KEY` - SECRET_KEY for the Django config
- Settings for sending e-mail:
    - `EMAIL_HOST`
    - `EMAIL_PORT`
    - `EMAIL_HOST_USER`
    - `EMAIL_HOST_PASSWORD`

### :coffee: Tests

Run all tests (run in the **publicnotes** folder):

```bash
./manage.py test wall.tests
```

Using `coverage`:

```bash
coverage run ./manage.py test wall.tests
```

With report page generation:

```bash
coverage run ./manage.py test wall.tests && coverage html
```

<a id="chapter-5"></a>

## :open_hands: License

If you use my code, put a star ⭐️ on the repository

Author: [Yu-Leo](https://github.com/Yu-Leo)

GNU General Public License v3.0

Full text in [LICENSE](LICENSE)
