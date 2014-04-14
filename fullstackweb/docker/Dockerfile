FROM    ubuntu:13.10

RUN apt-get -y install git
RUN apt-get update
RUN apt-get -y install gcc python-dev python-pip python-virtualenv python-software-properties software-properties-common nginx uwsgi curl nodejs npm
RUN apt-get -y install wget
RUN mkdir /deploy
RUN cd /deploy && git clone https://github.com/rorymurphy/exercises.git
RUN /deploy/exercises/fullstackweb/deploy/deploy_to_server
EXPOSE 80 8080