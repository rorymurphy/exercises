FROM    ubuntu:13.10

RUN apt-get -y install git
RUN mkdir /deploy
RUN cd /deploy && git clone https://github.com/rorymurphy/exercises.git
RUN less /deploy/exercises/fullstackweb/deploy/deploy_to_docker

EXPOSE 80 8080