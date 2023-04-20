FROM ubuntu:18.04    

RUN apt-get update -y && apt-get install -y python3-pip python3-dev git gcc g++    

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt   
COPY data.csv /app/data.csv
COPY assignment1.py .

RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt

CMD ["python3", "assignment1.py"]

VOLUME ["/app/output"]