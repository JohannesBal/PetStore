FROM python:3.9-alpine

RUN apk add --no-cache mariadb-connector-c-dev build-base mariadb mariadb-dev
RUN pip install --upgrade pip
RUN pip install Flask pyopenssl gunicorn mysql-connector-python mariadb

COPY ./app /app
WORKDIR /app

#VARS
ENV HOST=0.0.0.0
ENV WORKERS=4
ENV APP_NAME=flaskAPI

CMD [ "sh", "-c", "gunicorn ${APP_NAME}:app --bind ${HOST} --workers ${WORKERS}" ]
