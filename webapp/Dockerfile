FROM balenalib/raspberrypi3-python

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev
ENV PYTHONBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY webcam.py ./
COPY app.py ./

CMD ["python","./app.py"]
