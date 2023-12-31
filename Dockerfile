FROM ubuntu

RUN apt-get update 
RUN apt-get install -y bash
RUN apt-get install python3.11 -y
RUN apt-get install python3-pip python3-dev -y
RUN apt-get install libpq-dev -y

COPY . /service/

WORKDIR /service

RUN pip install -r requirements.txt 

# uvicorn main:run --host 0.0.0.0 --port 8100
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8100", "--ssl-keyfile", "/service/certs/cert.key", "--ssl-certfile", "/service/certs/cert.crt"]