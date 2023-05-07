FROM python:3.11-buster
WORKDIR /usr/src/app/amo

COPY requirements.txt /usr/src/app/amo"
RUN pip install -r /usr/src/app/amo/keys/requirements.txt
COPY keys /usr/src/app/amo/"