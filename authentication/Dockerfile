FROM python:3

RUN mkdir -p /opt/src/authentication_service
WORKDIR /opt/src/authentication_service

COPY ./authentication.py ./authentication.py
COPY ./configuration.py ./configuration.py
COPY ./models.py ./models.py
COPY ./requirements.txt ./requirements.txt
COPY ./bootstrap.py ./bootstrap.py
COPY ./bootstrap.sh ./bootstrap.sh

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/authentication_service"

ENTRYPOINT ["./bootstrap.sh"]
