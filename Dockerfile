FROM python:3.11-slim

RUN groupadd -r airflow && useradd -r -g airflow airflow
RUN mkdir -p /app /home/airflow
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh
RUN chmod -R 700 /home/airflow
RUN chown -R airflow:airflow /home/airflow
RUN chown -R airflow:airflow /app

USER airflow

ENV PATH="/home/airflow/.local/bin:$PATH"

WORKDIR /app
COPY --chown=airflow:airflow ./requirements.txt /app
RUN pip install -r requirements.txt
COPY app /app/app

ENTRYPOINT [ "/app/run.sh" ]