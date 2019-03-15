FROM ubuntu:latest

# tzdata ask region confirmation, use UTC
RUN apt-get update &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata &&\
    apt-get install -y libopencv-dev &&\
    apt-get install -y povray &&\
    apt-get install -y python3 &&\
    apt-get install -y python3-pip &&\
    pip3 install -y virtualenv
