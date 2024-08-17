FROM ubuntu:latest

WORKDIR /

COPY . .

ARG ENV
ARG HOST
ARG PORT
ARG DB_CONNECTION_URL


ENV ENV ${ENV}
ENV HOST ${HOST}
ENV PORT ${PORT}
ENV DB_CONNECTION_URL=${DB_CONNECTION_URL}


RUN apt update && apt install python3 python3-pip -y
RUN pip3 install -r requirements.txt --break-system-packages

CMD [ "python3", "main.py" ]
