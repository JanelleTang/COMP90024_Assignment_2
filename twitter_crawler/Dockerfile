FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

RUN sudo apt-get update && sudo apt-get install -y gdal-bin python-gdal python3-gdal

WORKDIR /code

ADD . /code

RUN pip install -r requirements_stream.txt