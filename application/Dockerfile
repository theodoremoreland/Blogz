FROM python:3.11-slim-buster

WORKDIR /application

RUN apt-get update
RUN apt-get -y install libpq-dev gcc

COPY . ./
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "application.py" ]