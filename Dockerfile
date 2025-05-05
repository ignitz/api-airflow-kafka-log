FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt

COPY app /app/app
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT [ "/app/run.sh" ]
