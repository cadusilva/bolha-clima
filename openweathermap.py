#!/usr/bin/python3

import json
import os
import math
import sys
import urllib.parse
import urllib.request
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q="
DEFAULT_CITY = "recife"
apiKey = os.getenv('OWM_API')

def try_city(city_name, apiKey):
    city_name = city_name.strip().rstrip("!?").replace("&apos;", "'").strip()

    full_api_url = (
        BASE_URL
        + urllib.parse.quote(city_name)
        + "&mode=json&units=metric&lang="
        + os.getenv('OWM_LANG')
        + "&APPID="
        + os.getenv('OWM_API')
    )

    try:
        with urllib.request.urlopen(full_api_url) as url:
            json_data = json.loads(url.read().decode("utf-8"))
    except urllib.request.HTTPError as exc:
        print("Erro na API: ", exc)
        return

    city = json_data.get("name")
    country = json_data.get("sys").get("country")
    weather = json_data.get("weather")[0].get("description")
    temp = json_data.get("main").get("temp")
    i_temp = math.floor(temp)
    feels_like = json_data.get("main").get("feels_like")
    i_feels_like = math.floor(feels_like)
    humidity = json_data.get("main").get("humidity")

    return f"o clima atual em {city}, {country} é esse: faz {i_temp} \xb0C com sensação térmica de {i_feels_like} \xb0C, {weather} e umidade do ar em {humidity}%."


if __name__ == "__main__":
    print(
        try_city(
            sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CITY,
            os.getenv('OWM_API'),
        )
    )
