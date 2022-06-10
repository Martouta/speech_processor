FROM martouta/ubuntu_python_playwright:v1.0.0

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
    && apt-get install -y ffmpeg \
    && apt-get install -y -q --no-install-recommends -o Dpkg::Options::="--force-confold" netcat \
    && mkdir /usr/src/app/log

CMD ["python3", "-u" , "."]
