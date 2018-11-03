FROM python:alpine3.7
MAINTAINER chorboon@gmail.com

COPY . .
WORKDIR .
RUN mkdir -p upload
RUN mkdir -p hash
RUN pip install -r requirements.txt
#RUN useradd -r -u 999 appuser
#USER appuser
EXPOSE 5000
CMD python ./file.py
