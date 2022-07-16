FROM python:3.10.4

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# Packages
RUN apt-get update && apt-get install -y gettext postgresql

# Requirements
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

RUN cd ./publicnotes  && django-admin compilemessages

RUN chmod u+x ./wait-for-postgres.sh

RUN python ./publicnotes/manage.py collectstatic --noinput