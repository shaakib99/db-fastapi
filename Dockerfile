FROM ubuntu:latest

WORKDIR /

COPY . .

ARG ENV
ARG HOST
ARG PORT
ARG REDIS_HOST
ARG REDIS_PORT

ENV ENV ${ENV}
ENV HOST ${HOST}
ENV PORT ${PORT}
ENV REDIS_HOST ${REDIS_HOST}
ENV REDIS_PORT ${REDIS_PORT}

RUN apt update && apt install python3 python3-pip -y
RUN pip3 install -r requirements.txt --break-system-packages

CMD [ "python3", "main.py" ]
