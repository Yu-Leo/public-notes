# Getting started

## General settings

1. Download this repository
   - Option 1
      1. Install [git](https://git-scm.com/download)
      2. Clone this repository
        ```bash
        git clone https://github.com/Yu-Leo/public-notes.git
        cd public-notes
        ```
   - Option 2 - [Download ZIP](https://github.com/Yu-Leo/public-notes/archive/refs/heads/main.zip)
2. Copy `/.env.example` to `/.env`, `/.env.dev` and `/.env.localdev`
   - `.env` file - for run project in **production** mode (using Docker compose)
   - `.env.dev` file - for run project in **development** mode (using Docker compose)
   - `.env.localdev` file - for development and run on a local machine:
3. Add your configurations in them
   - `DJANGO_DEBUG` - Run in DEBUG mode or not (set 1 or 0). Default 0.
   - `DJANGO_SECRET_KEY` - SECRET_KEY for the Django config
   - Settings for sending e-mail:
      - `EMAIL_HOST`
      - `EMAIL_PORT`
      - `EMAIL_HOST_USER`
      - `EMAIL_HOST_PASSWORD`
   - Settings for database (optional):
      - `DB_ENGINE` (default `django.db.backends.sqlite3`. For using PostgreSQL: `django.db.backends.postgresql`)
      - `DB_NAME` (default `os.path.join(BASE_DIR, 'db.sqlite3')`)
      - `DB_HOST`
      - `DB_PORT`
      - `DB_USER`
      - `DB_PASSWORD`
   - Settings for PostgreSQL (for run using Docker compose):
      - `POSTGRES_DB`
      - `POSTGRES_USER`
      - `POSTGRES_PASSWORD`

Now you can:

- Run in **production** mode using Docker compose
- Run in **development** mode using Docker compose
- Setting up for development and run on a local machine

## Run in **production** mode using Docker compose

```bash
docker-compose up --build
```

## Run in **development** mode using Docker compose

```bash
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build
```

## Setting up for development and run on a local machine

**SQLite3** will be used by default

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

## :arrow_left: [Back to README](../README.md)