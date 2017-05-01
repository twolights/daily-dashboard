FROM alpine:latest

ADD requirement.txt /tmp
ADD src /src

RUN apk update ; \
    apk add python python-dev py-setuptools git ; \
    easy_install-2.7 pip ; \
    pip install -r /tmp/requirement.txt ; \
    rm -f /tmp/requirement.txt 

WORKDIR /src/web
EXPOSE 5000

ENV FLASK_APP=app.py

ENTRYPOINT ["/usr/bin/flask", "run", "-h", "0.0.0.0"]
