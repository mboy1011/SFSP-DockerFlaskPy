FROM mysql:5.7

LABEL maintainer="Lyjieme Barro"

EXPOSE 3306
CMD ["mysqld"]  

FROM python:3-buster
# Place app in container.
COPY ./www /opt/www
WORKDIR /opt/www

# Install dependencies.
RUN pip3 install -r requirements.txt

RUN apt update && apt full-upgrade -y && apt install python3-mysqldb

EXPOSE 80
CMD python3 controller.py