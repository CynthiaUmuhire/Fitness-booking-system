FROM python:alpine

RUN mkdir /code
WORKDIR /code
COPY . /code

RUN apk add python3-dev build-base linux-headers pcre-dev sshpass
RUN pip install uwsgi
RUN pip3 install -r requirements.txt


# Set environment variables 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1
ENV DEBUD = False

EXPOSE 8000

RUN mkdir /var/run/app-uwsgi
RUN chmod -R 777 /var/run/app-uwsgi

CMD ["uwsgi", "--ini", "/code/mysite.uwsgi.ini"]

