FROM python:3.15.0a7-alpine3.22
RUN apk add g++ libffi-dev mariadb-dev
RUN mkdir /app
ADD requirements.txt /app
RUN pip install -r /app/requirements.txt
ADD src /app/src
ADD static /app/static
ADD main.py /app
WORKDIR /app
CMD ["python3","/app/main.py"]