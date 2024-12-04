FROM python:3.12

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /usr/src/install

COPY requirements.txt /usr/src/install/
RUN pip install --no-cache-dir -r /usr/src/install/requirements.txt

WORKDIR /usr/src/app

ENTRYPOINT [ "python", "entrypoint.py" ]
