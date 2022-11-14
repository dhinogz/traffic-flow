# pull official base image
FROM python:3.10

# set working directory
WORKDIR /usr/src/traffic_flow

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc \
    && apt-get clean

# add app
COPY traffic_flow/ .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
