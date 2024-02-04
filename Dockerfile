FROM python:slim
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /app

COPY openweathermap.py .
COPY under_the_weather.py .
COPY LICENSE .

RUN pip3 install python-dotenv lxml mastodon.py unidecode spacy \
    --no-cache-dir --upgrade && \
    python3 -m spacy download pt_core_news_md && \
    sed -i 's/os.getenv/os.environ.get/g' under_the_weather.py

CMD [ "python3", "under_the_weather.py" ]
