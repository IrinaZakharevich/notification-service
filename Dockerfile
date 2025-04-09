FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
