# Dashboard Consumer
Real-time dashboard consumer demo api

Build the image:
```
$ docker-compose build
```

Once the image is built, run the container:
```
$ docker-compose up -d
```
Currently the consumer builds with gunicorn server.
If you want to run tests/debug, comment out the last line in 
dockerfile and replace it with the linejust above it.
 Also rebuild after.
```
CMD ["python", "consumer.py"]
#ENTRYPOINT ["gunicorn", "--config=gunicorn_config.py", "wsgi:app"]
```