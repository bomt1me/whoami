FROM python:latest

WORKDIR /whoami
COPY . .

RUN apt-get update \
    && pip install poetry \
    && poetry install
