FROM python:3.7-slim

COPY . /root

WORKDIR /root

RUN apt-get -y update
RUN apt-get install -y libsndfile1
RUN apt-get install -y ffmpeg

RUN pip install -r requirements.txt
