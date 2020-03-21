# A simple Flask app container.
FROM mysql:5.7
FROM python:3-buster
LABEL maintainer="Lyjieme Barro"

# Place app in container.
COPY ./www /opt/www
WORKDIR /opt/www

# Install dependencies.
RUN pip3 install -r /opt/www/requirements.txt

RUN apt update && apt full-upgrade -y && apt install python3-mysqldb

EXPOSE 80

#################################
