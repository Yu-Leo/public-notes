FROM python:3.10.4

WORKDIR /usr/src/app/

COPY . /usr/src/app

# Dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Translations
RUN apt-get update && apt-get install -y gettext
RUN cd ./publicnotes  && django-admin compilemessages