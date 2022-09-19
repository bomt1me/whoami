FROM node:latest

WORKDIR /front
COPY ./front .

RUN apt-get update \
	&& npm install -g @angular/cli
