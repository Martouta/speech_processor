FROM python:3.10-slim

SHELL ["/bin/bash", "-c"]

WORKDIR /usr/src/app

COPY requirements.txt __main__.py .
COPY app app
COPY audio_chunks audio_chunks
COPY audios audios
COPY config config
COPY subtitles subtitles
COPY videos videos

RUN pip3 install --no-cache-dir -r requirements.txt \
    && apt-get -y update && apt-get -y upgrade && apt-get -y autoremove \
    && apt-get install -y ffmpeg \
    && apt-get install -y -q --no-install-recommends -o Dpkg::Options::="--force-confold" netcat \
    && mkdir /usr/src/app/log

CMD ["python3", "-u" , "."]
