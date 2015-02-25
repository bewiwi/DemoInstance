FROM ubuntu:14.04
MAINTAINER Loïc PORTE
RUN apt-get update &&\
    apt-get install \
    git python python-dev python-pip mysql-client\
    libmysqlclient-dev nodejs npm libldap2-dev\
    libsasl2-dev libssl-dev -y
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower grunt-cli
RUN mkdir /opt/demoinstance

VOLUME /opt/demoinstance

WORKDIR /opt/demoinstance
ENTRYPOINT pip install -r requirements.txt &&\
    pip install -r test/requirements.txt &&\
    cd /opt/demoinstance/web &&\
    npm install &&\
    bower install --allow-root &&\
    grunt && cd /opt/demoinstance/ &&\
    python demo.py -c test/samples/config/config-fake.ini
EXPOSE 8080
