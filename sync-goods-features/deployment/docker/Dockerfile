FROM ubuntu:20.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    python3-pip

# MSSQL drivers setup https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017#ubuntu17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN apt-get install -y unixodbc-dev
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN source ~/.bashrc
# optional: for unixODBC development headers
RUN apt-get install -y unixodbc-dev

RUN odbcinst -j

##
# Application sources and setup
##
ENV APP_HOME=/sync-goods-features
ENV SOURCES_DIR=sync_goods_features

COPY $SOURCES_DIR $APP_HOME/$SOURCES_DIR
COPY requirements.txt $APP_HOME
COPY deployment/docker/start.sh $APP_HOME

WORKDIR $APP_HOME

RUN pip3 install -r requirements.txt

RUN chmod +x ./start.sh

CMD ["./start.sh"]