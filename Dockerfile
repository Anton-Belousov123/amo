FROM python:3.11-buster
WORKDIR /usr/src/app/amo
COPY . .
RUN ls -R /usr/src/app/amo && \
    pip install -r misc/requirements.txt && \
    ls -R /usr/src/app/amo
