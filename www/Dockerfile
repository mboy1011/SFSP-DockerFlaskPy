# A simple Flask app container.
FROM python:3-buster
LABEL maintainer="Lyjieme Barro"

# Place app in container.
COPY . /opt/www
WORKDIR /opt/www

# Install dependencies.
RUN pip3 install -r requirements.txt

RUN apt update && apt full-upgrade -y && apt install python3-mysqldb

EXPOSE 80
CMD python3 controller.py