FROM python:alpine3.7
MAINTAINER chorboon@gmail.com

COPY . .
WORKDIR .
RUN mkdir -p upload
RUN pip install -r requirements.txt
RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser
USER appuser
EXPOSE 5000
CMD python ./file.py
