FROM martouta/ubuntu_python_playwright:v1.0.0

SHELL ["/bin/bash", "-c"]

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements-dev.txt \
    && apt-get install -y vim \
    && apt-get install -y -q --no-install-recommends -o Dpkg::Options::="--force-confold" netcat

RUN head -n 166 /usr/local/lib/python3.10/dist-packages/TikTokApi/tiktok.py > tmp.txt \
    && echo "            print(type(self._browser))" >> tmp.txt \
    && tail -n +166 /usr/local/lib/python3.10/dist-packages/TikTokApi/tiktok.py >> tmp.txt \
    && cat tmp.txt > /usr/local/lib/python3.10/dist-packages/TikTokApi/tiktok.py \
    # && rm tmp.txt
