# ============= COMP90024 - Assignment 2 ============= #
#                               
# The University of Melbourne           
# Team 37
#
# ** Authors: **
# 
# JJ Burke              1048105
# Janelle Tang          694209
# Shuang Qiu            980433
# Declan Baird-Watson   640975
# Avinash Rao           1024577 
# 
# Location: Melbourne
# ==================================================== 

FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

RUN apt-get update && apt-get install -y gdal-bin python-gdal python3-gdal

WORKDIR /code

ADD . /code

RUN pip install -r requirements_stream.txt
