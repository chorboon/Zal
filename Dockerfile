FROM python:alpine3.7
MAINTAINER chorboon@gmail.com

COPY . .
WORKDIR .
RUN mkdir -p upload
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./file.py
