FROM python:3

RUN mkdir -p /opt/src/authentication_service
WORKDIR /opt/src/authentication_service

COPY ./authentication.py ./authentication.py
COPY ./configuration.py ./configuration.py
COPY ./models.py ./models.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

EXPOSE 5002

ENV PYTHONPATH="/opt/src/authentication_service"

CMD ["python", "authentication.py"]
