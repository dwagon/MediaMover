FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install make
RUN apt-get -y install python3
RUN apt-get -y install python3-venv

RUN mkdir /build
ADD . /build
WORKDIR /build
ENV WORKON_HOME=/tmp
RUN make venv
