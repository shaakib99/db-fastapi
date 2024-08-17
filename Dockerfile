FROM ubuntu:latest

WORKDIR /

COPY . .

ARG ENV
ARG HOST
ARG PORT=8001
ARG DB_CONNECTION_URL


ENV ENV ${ENV}
ENV HOST ${HOST}
ENV PORT ${PORT}
ENV DB_CONNECTION_URL ${DB_CONNECTION_URL}

RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  pkg-config \
  gcc \
  pkg-config 
RUN apt install python3 python3-pip -y
RUN pip3 install -r requirements.txt --break-system-packages

EXPOSE ${PORT}

CMD [ "python3", "main.py" ]
