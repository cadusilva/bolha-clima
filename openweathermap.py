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
        + "&elements=temp,feelslike,humidity,uvindex,conditions,datetime,cloudcover,precipprob,windspeed,sunrise,sunset,timezone&key="
        + api_key
    )

    try:
        with urllib.request.urlopen(full_api_url) as url:
            json_data = json.loads(url.read().decode("utf-8"))
    except urllib.request.HTTPError as exc:
        return exc.code

    city        = json_data.get("resolvedAddress")
    tz          = json_data.get("timezone")
    weather     = json_data.get("currentConditions").get("conditions").lower()
    temp        = json_data.get("currentConditions").get("temp")
    feelslike   = json_data.get("currentConditions").get("feelslike")
    humidity    = json_data.get("currentConditions").get("humidity")
    uvindex     = json_data.get("currentConditions").get("uvindex")
    rain        = json_data.get("currentConditions").get("precipprob")
    clouds      = json_data.get("currentConditions").get("cloudcover")
    time        = json_data.get("currentConditions").get("datetime")[:5]
    wind        = json_data.get("currentConditions").get("windspeed")
    sunrise     = json_data.get("currentConditions").get("sunrise")[:5]
    sunset      = json_data.get("currentConditions").get("sunset")[:5]

    i_temp      = round(Decimal(temp))
    i_feelslike = round(Decimal(feelslike))
    i_humidity  = "{:.0f}".format(humidity)
    i_uvindex   = "{:.0f}".format(uvindex)
    i_rain      = "{:.0f}".format(rain)
    i_clouds    = "{:.0f}".format(clouds)

    return f"esse é o clima em {city} às {time}\n:temp: Temperatura: {i_temp} \xb0C\n:s_termica: Sensação térmica: {i_feelslike} \xb0C\n:ceu: Céu agora: {weather}, {i_clouds}% encoberto\n\nInformações adicionais:\n:sunny: Índice UV: {i_uvindex}/10\n:umidade: Umidade do ar: ~{i_humidity}%\n:rain: Chances de chover: ~{i_rain}%\n:nascerSol: Nascer do sol: {sunrise}\n:porSol: Pôr do sol: {sunset}\n:vento: Velocidade do vento: {wind} km/h\n\U0001f551 Fuso horário: {tz}\n\n#clima #BolhaClima"

if __name__ == "__main__":
    DEFAULT_CITY = "recife"
    load_dotenv()
    print(
        try_city(
            sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CITY,
            os.getenv("WTH_API"),
        )
    )
