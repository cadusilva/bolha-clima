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

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
executor = concurrent.futures.ThreadPoolExecutor()
logger = logging.getLogger(__name__)

def try_city(city_name, api_key: str, lang="pt", timeout: int = None) -> typing.Union[str, int]:
    city_name = city_name.strip().rstrip("!?").replace("&apos;", "'").strip()

    full_api_url = (
        BASE_URL
        + urllib.parse.quote(city_name)
        + "/?unitGroup=metric&include=current&lang="
        + lang
        + "&contentType=json&key="
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
    
    lat         = json_data.get("latitude")
    lon         = json_data.get("longitude")

    location    = json_data.get("resolvedAddress")
    weather     = json_data.get("currentConditions").get("conditions").lower()
    temp        = json_data.get("currentConditions").get("temp")
    feelslike   = json_data.get("currentConditions").get("feelslike")
    humidity    = json_data.get("currentConditions").get("humidity")
    clouds      = json_data.get("currentConditions").get("cloudcover")
    uvIndex     = json_data.get("currentConditions").get("uvindex")
    precipprob  = json_data.get("currentConditions").get("precipprob")
    datetime    = json_data.get("currentConditions").get("datetime")[:2]

    i_temp          = round(Decimal(temp))
    i_feelslike     = round(Decimal(feelslike))
    i_clouds        = round(Decimal(clouds))
    i_humidity      = round(Decimal(humidity))
    i_uvIndex       = round(Decimal(uvIndex))
    i_precipprob    = round(Decimal(precipprob))

    amanhaMax       = json_data.get("days")[1].get("tempmax")
    sensacaoMax     = json_data.get("days")[1].get("feelslikemax")
    amanhaRain      = json_data.get("days")[1].get("precipprob")

    i_amanhaMax     = round(Decimal(amanhaMax))
    i_sensacaoMax   = round(Decimal(sensacaoMax))
    i_amanhaRain    = round(Decimal(amanhaRain))

    return f"O clima em {location} às {datetime}h é:\n\n:temp: Temperatura: {i_temp} \xb0C\n:s_termica: Sensação térmica: {i_feelslike} \xb0C\n:sunny: Índice UV: {i_uvIndex} de 11\n:ceu: Céu agora: {weather}, {i_clouds}% encoberto, {i_precipprob}% de chances de chuva\n:umidade: Umidade do ar: {i_humidity}%\n\n\U0001f4c5 Para amanhã, a temperatura pode alcançar {i_amanhaMax} \xb0C com sensação térmica de até {i_sensacaoMax} \xb0C e {i_amanhaRain}% de chances de chover.\n\n\U0001f4cd Ver cidade no mapa: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}\n\u2139\uFE0F Com informações de VisualCrossing\n\u231A O horário mencionado é o da cidade pesquisada.\n\n#clima #BolhaClima"


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
