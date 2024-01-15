FROM debian:stable-slim
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install python3 python3-pip --no-install-recommends -y
RUN pip3 install python-dotenv lxml mastodon.py spacy --no-cache-dir --upgrade --break-system-packages
RUN python3 -m spacy download pt_core_news_md --break-system-packages

WORKDIR /usr/app/clima
COPY openweathermap.py ./
COPY under_the_weather.py ./
COPY LICENSE ./
RUN sed -i 's/os.getenv/os.environ.get/g' under_the_weather.py
CMD [ "python3", "./under_the_weather.py" ]