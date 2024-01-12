FROM python:slim
RUN pip3 install --no-cache-dir --upgrade python-dotenv lxml mastodon.py spacy
RUN python3 -m spacy download pt_core_news_md

WORKDIR /usr/app/clima
COPY openweathermap.py ./
COPY under_the_weather.py ./
COPY LICENSE ./
RUN sed -i 's/os.getenv/os.environ.get/g' under_the_weather.py
CMD [ "python3", "./under_the_weather.py" ]