FROM python:3.11-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
