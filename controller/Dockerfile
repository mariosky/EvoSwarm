FROM python:3.7-alpine
RUN apk --no-cache add --virtual .builddeps gcc gfortran musl-dev

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN chmod 644 controller.py
