FROM python:3.9-alpine as builder

RUN apk add --no-cache mariadb-connector-c-dev build-base mariadb mariadb-dev

WORKDIR /app
COPY ./app /app
RUN pip install --upgrade pip \
 && pip install --no-cache-dir Flask gunicorn mysql-connector-python mariadb

FROM python:3.9-alpine

WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY --from=builder /usr/lib/libmariadb.so* /usr/lib/
COPY --from=builder /app /app

ENV HOST=0.0.0.0
ENV WORKERS=4
ENV APP_NAME=flaskAPI

CMD ["sh", "-c", "gunicorn ${APP_NAME}:app --bind ${HOST} --workers ${WORKERS}"]
