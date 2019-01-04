FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["gunicorn", "wsgi:app", "--worker-class=sanic.worker.GunicornWorker", "-b=:8000", "--workers=4"]

EXPOSE 8000
