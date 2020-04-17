FROM python:3.7-alpine
# See: https://hub.docker.com/_/python

# Set the working directory to /app
# WORKDIR /usr/src/app

# no-cache-dir to reduce image size
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

CMD [ "python", "src/app.py"]
