FROM python:3.11-buster
WORKDIR /usr/src/app/amo
COPY . .
RUN pip install -r misc/requirements.txt
