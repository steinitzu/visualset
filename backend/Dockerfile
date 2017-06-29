FROM python:3.6.1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8000

# CMD ["gunicorn", "web:app",  "-k", "gevent"]
