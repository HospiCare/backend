FROM python:3.12-slim

WORKDIR /backend

RUN apt-get update
RUN apt-get install make pkg-config python3-dev default-libmysqlclient-dev build-essential libzbar-dev netcat-traditional -y

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

COPY . .

ENTRYPOINT ["sh", "./entrypoint.sh"]
