FROM python:3.11-slim-buster

WORKDIR /application

RUN apt-get update
RUN apt-get -y install libpq-dev gcc

COPY application/ ./
RUN pip install -r requirements.txt


CMD [ "python", "application.py" ]