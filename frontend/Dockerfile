FROM python:3.7-alpine
# See: https://hub.docker.com/_/python

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    rm -rf /var/cache/apk/*

RUN apk add g++

# no-cache-dir to reduce image size
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ /src/

ENTRYPOINT ["python"]
CMD ["src/app.py"]
