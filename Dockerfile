FROM apache/airflow:2.9.1

USER root

COPY requirements.txt /requirements.txt

# Install as airflow user to comply with Airflow's guidelines
RUN chown airflow: /requirements.txt

USER airflow

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r /requirements.txt

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt


