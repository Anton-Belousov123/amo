FROM python:3.11-buster
WORKDIR /usr/src/app/amo

COPY misc/requirements.txt /usr/src/app/amo/misc
RUN pip install -r /usr/src/app/amo/misc/requirements.txt
COPY . /usr/src/app/amo/
