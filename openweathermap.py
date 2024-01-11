#!/usr/bin/python3
"""
    This file is part of under_the_weather.

    Copyright (C) 2018 Dan Soucy <dev@danso.ca>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import concurrent.futures
import json
import logging
import os
import sys
import typing
import urllib.parse
import urllib.request

from dotenv import load_dotenv
from decimal import Decimal

BASE_URL = "https://api.weatherapi.com/v1/current.json?q="
executor = concurrent.futures.ThreadPoolExecutor()
logger = logging.getLogger(__name__)


def try_city(city_name, api_key: str, lang="pt", timeout: int = None) -> typing.Union[str, int]:
    city_name = city_name.strip().rstrip("!?").replace("&apos;", "'").strip()

    full_api_url = (
        BASE_URL
        + urllib.parse.quote(city_name)
        + "&aqi=no&lang="
        + lang
        + "&key="
        + api_key
    )

    try:
        json_data = executor.submit(_read_json, full_api_url).result(timeout=timeout)
    except urllib.request.HTTPError as exc:
        return exc.code
    except concurrent.futures.TimeoutError:
        return 429
    except:
        logger.exception("Algo inesperado aconteceu.")
        return 500

    updated     = json_data.get("current").get("last_updated")[-5:]
    city        = json_data.get("location").get("name")
    region      = json_data.get("location").get("region")
    country     = json_data.get("location").get("country")
    weather     = json_data.get("current").get("condition").get("text").lower()
    temp        = json_data.get("current").get("temp_c")
    feelslike   = json_data.get("current").get("feelslike_c")
    humidity    = json_data.get("current").get("humidity")
    clouds      = json_data.get("current").get("cloud")
    uv          = json_data.get("current").get("uv")

    lat         = json_data.get("location").get("lat")
    lon         = json_data.get("location").get("lon")

    i_temp      = round(Decimal(temp))
    i_feelslike = round(Decimal(feelslike))
    i_uv        = round(Decimal(uv))
#    i_humidity  = "{:.0f}".format(humidity)
#    i_clouds    = "{:.0f}".format(clouds)

    return f"Esse é o clima atual em {city} ({region}, {country}):\n\n:temp: Temperatura: {i_temp} \xb0C\n:s_termica: Sensação térmica: {i_feelslike} \xb0C\n:ceu: Céu agora: {weather}, {clouds}% encoberto\n:umidade: Umidade do ar: {humidity}%\n:sunny: Índice UV: {i_uv} de 11\n\n\U0001f552 Atualizado às {updated} (horário local)\n\U0001f5fa\uFE0F Ver cidade no mapa: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}\n\u2139\uFE0F Com informações de WeatherAPI\n\n#clima #BolhaClima"


def _read_json(url):
    with urllib.request.urlopen(url) as doc:
        return json.loads(doc.read().decode())


if __name__ == "__main__":
    DEFAULT_CITY = "recife"
    load_dotenv()
    print(
        try_city(
            sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CITY,
            os.getenv("WTH_API"),
        )
    )
