FROM python:3.10
MAINTAINER Oskar Laasik <oskar.laasik@yahoo.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/consumer/src
# We copy the requirements.txt file first to avoid cache invalidations
COPY requirements.txt /opt/services/consumer/src/
WORKDIR /opt/services/consumer/src
RUN pip install -r requirements.txt
COPY . /opt/services/consumer/src
EXPOSE 5090
#CMD ["python", "consumer.py"]
ENTRYPOINT ["gunicorn", "--config=gunicorn_config.py", "wsgi:app"]



