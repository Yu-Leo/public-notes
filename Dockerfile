FROM python:3.10

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

# Requirements
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . /usr/src/app
