FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install tensorflow --no-cache-dir
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN chmod +x /app/server/route.py

CMD ["python3", "/app/server/route.py"]
