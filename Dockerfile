FROM python:3.7-alpine

RUN apk add make
RUN apk add --no-cache gcc libc-dev git libffi-dev openssl-dev

RUN mkdir /usr/src/code
WORKDIR /usr/src/code

ENV PYTHONPATH /usr/src/code

COPY barmaid/requirements/common.txt .
RUN pip3 install -r common.txt

RUN apk del gcc libc-dev git libffi-dev openssl-dev
COPY . .

# RUN make migrate

ENV PYTHONUNBUFFERED 1
ENV NAME barmaid