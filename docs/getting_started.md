## :hammer: Getting started

1. Download this repository
    - Option 1
        1. Install [git](https://git-scm.com/download)
        2. Clone this repository
         ```bash
         git clone https://github.com/Yu-Leo/public-notes.git
         cd public-notes
         ```
    - Option 2 - [Download ZIP](https://github.com/Yu-Leo/public-notes/archive/refs/heads/main.zip)
2. Set the values of the [required environment variables](#envvars)
    - Create `.env` file with values for **production** mode
    - Create `.env.dev` file with values for **development** mode

Now you can:

- Run in **production** mode using docker-compose
- Run in **development** mode using docker-compose
- Setting up for development and run on a local machine

### Run in **production** mode using docker-compose:

```bash
docker-compose up --build
```

### Run in **development** mode using docker-compose:

```bash
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build
```

### Setting up for development and run on a local machine:

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