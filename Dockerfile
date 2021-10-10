FROM martouta/python_audio_google_cloud:v2

SHELL ["/bin/bash", "-c"]

RUN apt-get -y update && apt-get -y upgrade && apt-get -y autoremove \
    && apt-get install -y -q --no-install-recommends -o Dpkg::Options::="--force-confold" netcat

WORKDIR /usr/src/app
COPY . /usr/src/app
