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

import json
import os
import sys
import typing
import urllib.parse
import urllib.request

from dotenv import load_dotenv
from decimal import Decimal

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


def try_city(city_name, api_key: str, lang="pt") -> typing.Union[str, int]:
    city_name = city_name.strip().rstrip("!?").replace("&apos;", "'").strip()

    full_api_url = (
        BASE_URL
        + urllib.parse.quote(city_name)
        + "/?unitGroup=metric&include=current&lang="
        + lang
        + "&elements=temp,feelslike,humidity,uvindex,conditions,datetime,cloudcover,precipprob,description,tempmax,tempmin,feelslikemax,severerisk&key="
        + api_key
    )

    try:
        with urllib.request.urlopen(full_api_url) as url:
            json_data = json.loads(url.read().decode("utf-8"))
    except urllib.request.HTTPError as exc:
        return exc.code

    # hoje
    city        = json_data.get("resolvedAddress")
    weather     = json_data.get("currentConditions").get("conditions").lower()
    temp        = json_data.get("currentConditions").get("temp")
    feelslike   = json_data.get("currentConditions").get("feelslike")
    humidity    = json_data.get("currentConditions").get("humidity")
    uvindex     = json_data.get("currentConditions").get("uvindex")
    rain        = json_data.get("days")[0].get("precipprob")
    clouds      = json_data.get("currentConditions").get("cloudcover")
    time        = json_data.get("currentConditions").get("datetime")[:5]

    # amanhã
    temp_max    = json_data.get("days")[0].get("tempmax")
    temp_min    = json_data.get("days")[0].get("tempmin")
    feelslike_a = json_data.get("days")[0].get("feelslikemax")
    descricao   = json_data.get("days")[0].get("description").lower()
    severo      = json_data.get("days")[0].get("severerisk")

    # hoje
    i_temp      = round(Decimal(temp))
    i_feelslike = round(Decimal(feelslike))
    i_humidity  = "{:.0f}".format(humidity)
    i_uvindex   = "{:.0f}".format(uvindex)
    i_rain      = "{:.0f}".format(rain)
    i_clouds    = "{:.0f}".format(clouds)

    # amanhã
    i_temp_max      = round(Decimal(temp_max))
    i_temp_min      = round(Decimal(temp_min))
    i_feelslike_a   = round(Decimal(feelslike_a))
    i_severo        = round(Decimal(severo))

    return f"Esse é o clima em {city} às {time} (horário local):\n\n:temp: Temperatura: {i_temp} \xb0C\n:s_termica: Sensação térmica: {i_feelslike} \xb0C\n:ceu: Céu agora: {weather}, {i_clouds}% encoberto\n:sunny: Índice UV: {i_uvindex}/10\n:umidade: Umidade do ar: ~{i_humidity}%\n:rain: Chances de chover hoje: ~{i_rain}%\n\n\U0001f4c6 Para amanhã poderemos ter máxima de {i_temp_max} \xb0C, mínima de {i_temp_min} \xb0C e sensação de até {i_feelslike_a} \xb0C com céu {descricao} Há {i_severo}% de chances de clima severo.\n\n#clima #BolhaClima"

if __name__ == "__main__":
    DEFAULT_CITY = "recife"
    load_dotenv()
    print(
        try_city(
            sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CITY,
            os.getenv("WTH_API"),
        )
    )
