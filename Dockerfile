#USING python:3.8-slim as base image to reduce size
FROM python:3.8-slim

# install google chrome
RUN apt-get -y update && apt-get install -y \
    gnupg2 \
    wget \
    curl && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update && \
    apt-get install -y google-chrome-stable && \
    # install chromedriver
    apt-get install -yqq unzip  && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ $$ \
    rm -rf /tmp/chromedriver.zip && \
    # upgrade pip,# install selenium
    pip install --upgrade pip && \
    pip install selenium && \
    pip install requests

# set display port to avoid crash
ENV DISPLAY=:99

# copy app/run.py file from local
COPY app/run.py /

#build docker: docker build -t milan-img:latest -t milan-img:0.1 .
#tag: docker tag milan-img liulirun/milan-img
#push: docker image push liulirun/milan-img:latest