FROM python:3.12-alpine3.20
RUN apk add --no-cache \
    g++ \
    libffi-dev \
    mariadb-dev \
    gcc \
    musl-dev \
    mariadb-connector-c-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY static/ ./static/
COPY main.py .

CMD ["python3","/app/main.py"]
