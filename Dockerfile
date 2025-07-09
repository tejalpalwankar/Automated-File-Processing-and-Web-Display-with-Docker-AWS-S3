FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install flask boto3

EXPOSE 80
CMD ["python", "app.py"]
