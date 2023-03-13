FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install tensorflow --no-cache-dir
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

CMD ["python3", "/app/serve.py"]
