# pull official base image
FROM python:3.10

# set working directory
WORKDIR /usr/src/test-agent

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc \
    && apt-get clean

# add app
COPY test-agent/ .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
