FROM python:3.7
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

RUN python3 -m pip install --upgrade pip && apt-get update && apt-get install -y fluidsynth 

COPY ./requirements.txt /workspace/

RUN python3 -m pip install -r /workspace/requirements.txt

CMD python manage.py runserver 0.0.0.0:8000