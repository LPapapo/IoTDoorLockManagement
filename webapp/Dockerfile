FROM balenalib/raspberrypi3-python:3.9-bullseye

RUN install_packages default-libmysqlclient-dev
ENV PYTHONBUFFERED 1
RUN pip install  setuptools wheel
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt --extra-index-url=https://www.piwheels.org/simple

COPY webcam.py ./
COPY app.py ./

CMD ["python","./app.py"]