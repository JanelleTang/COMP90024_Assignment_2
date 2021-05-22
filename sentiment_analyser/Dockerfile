FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

RUN sudo apt-get update && sudo apt-get install -y gdal-bin python-gdal python3-gdal

WORKDIR /code

ADD . /code/sentiment_analyser

ADD ../twitter_crawler /code/twitter_crawler

RUN pip install -r requirements.txt