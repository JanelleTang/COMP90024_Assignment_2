FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

RUN apt-get update && apt-get install -y gdal-bin python-gdal python3-gdal libsqlite3-mod-spatialite

WORKDIR /code

ADD . /code

RUN pip install -r requirements.txt