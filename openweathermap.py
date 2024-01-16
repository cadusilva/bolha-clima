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

from unidecode import unidecode
from dotenv import load_dotenv
from decimal import Decimal

BASE_URL = "https://wttr.in/"
executor = concurrent.futures.ThreadPoolExecutor()
logger = logging.getLogger(__name__)

def try_city(city_name, api_key: str, lang="pt", timeout: int = None) -> typing.Union[str, int]:
    city_name = city_name.strip().rstrip("!?").replace("&apos;", "'").strip()
    city_name = unidecode(city_name)

    full_api_url = (
        BASE_URL
        + urllib.parse.quote(city_name)
        + "?m&lang="
        + lang
        + "&format=j1"
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
    
    lat         = json_data.get("nearest_area")[0].get("latitude")
    lon         = json_data.get("nearest_area")[0].get("longitude")

    city        = json_data.get("nearest_area")[0].get("areaName")[0].get("value")
    state       = json_data.get("nearest_area")[0].get("region")[0].get("value")
    country     = json_data.get("nearest_area")[0].get("country")[0].get("value")
    weather     = json_data.get("current_condition")[0].get("lang_" + os.getenv("WTH_LANG") )[0].get("value").lower()
    temp        = json_data.get("current_condition")[0].get("temp_C")
    feelslike   = json_data.get("current_condition")[0].get("FeelsLikeC")
    humidity    = json_data.get("current_condition")[0].get("humidity")
    clouds      = json_data.get("current_condition")[0].get("cloudcover")
    uvIndex     = json_data.get("current_condition")[0].get("uvIndex")

    i_temp      = round(Decimal(temp))
    i_feelslike = round(Decimal(feelslike))
    
    minAmanha   = json_data.get("weather")[1].get("mintempC")
    avgAmanha   = json_data.get("weather")[1].get("avgtempC")
    maxAmanha   = json_data.get("weather")[1].get("maxtempC")

    return f"Esse é o clima atual em {city} ({state}, {country}):\n\n:temp: Temperatura: {i_temp} \xb0C\n:s_termica: Sensação térmica: {i_feelslike} \xb0C\n:sunny: Índice UV: {uvIndex} de 11\n:ceu: Céu agora: {weather}, {clouds}% encoberto\n:umidade: Umidade do ar: {humidity}%\n\n\U0001f4c6 Para amanhã, a temperatura média deve ser de {avgAmanha} \xb0C, com mínima de {minAmanha} \xb0C e máxima de {maxAmanha} \xb0C.\n\n\U0001f4cd Ver cidade no mapa: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}\n\u2139\uFE0F Com informações de wttr.in\n\n#clima #BolhaClima"


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
