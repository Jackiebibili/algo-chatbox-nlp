FROM python:3.9-alpine

COPY . /code
WORKDIR /code

RUN chmod +x ./hostscript

ENTRYPOINT ./hostscript