FROM alpine:3.13.5

LABEL name='urlshortener'
LABEL version='1.0.1'

RUN apk update && apk add build-base python3-dev py3-pip

WORKDIR /workspace
ADD ./requirements.txt /workspace/requirements.txt
RUN pip3 install -r requirements.txt
ADD . /workspace

EXPOSE 5000

CMD ["gunicorn",  "--bind",  "0.0.0.0:5000",  "wsgi:app"]
