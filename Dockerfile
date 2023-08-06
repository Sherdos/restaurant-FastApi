FROM python:3.10-slim

RUN mkdir /restaurant_fastapi

WORKDIR /restaurant_fastapi

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x docker/app.sh
