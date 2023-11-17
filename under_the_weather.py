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

import os

from dotenv import load_dotenv
from lxml import etree
from mastodon import Mastodon, StreamListener
import spacy

from openweathermap import try_city


class StreamListenerWeather(StreamListener):
    def __init__(self, mastodon: Mastodon):
        self.apikey = os.getenv("WTH_API")
        self.lang = os.getenv("WTH_LANG")
        self.mastodon = mastodon
        self.nlp = spacy.load(os.getenv("UTW_NER_MODEL"))
        self.false_loc = ("legal",)
        super().__init__()

    def on_update(self, status):
        name = status.get("account", {}).get("acct")
        print(f"Status recebido de {name}.")
        if name == "UnderTheWeather":
            print("é apenas um feedback!")

    def on_notification(self, notification):
        print("Nova notificação!")
        acct = notification.get("account").get("acct")
        notif_type = notification.get("type")
        if notif_type == "reblog":
            print(f"Toot foi impulsionado por @{acct}")
            return
        elif notif_type == "favourite":
            print(f"Toot foi favoritado por @{acct}")
            return
        elif notif_type == "follow":
            print(f"Novo seguidor: @{acct}")
            return
        elif notif_type != "mention":
            print("Que esquisito, um tipo de notificação desconhecido.")
            return

        status = notification.get("status")
        if status is None:
            print("O status estava vazio.")
            return

        visibility = status.get("visibility")
        if visibility == "public":
            visibility = "unlisted"

        content = status.get("content")
        if content is None:
            print("O conteúdo estava vazio.")
            return

        print("A mensagem é: " + content)
        # Valid example content (line break added for readability):
        # <p><a href="https://bolha.one/@cadusilva" class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@cadusilva</a>
        # <span> </span>
        # <a href="https://bolha.one/@clima" class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@clima</a>
        # <span> São Paulo</span></p>
        #
        # Invalid example content (line break added for readability):
        # <p><span class="h-card">
        # <a href="https://bolha.one/@clima" class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@
        # <span>clima</span></a>
        # </span> </p>
        # <p>Como ta o clima em viçosa?</p>

        content = etree.XML(f"<div>{content}</div>").xpath("string()")

        msg = " ".join((w for w in content.split() if not w.startswith("@")))

        if not msg:
            self.mastodon.status_post(
                f"@{acct} quer me dizer alguma coisa?",
                in_reply_to_id=status,
                visibility=visibility,
            )
            return

        # Perform NER to extract city names from complete sentences
        places = [e for e in self.nlp(msg).ents if e.label_ == "LOC"]
        if places:
            print("Localidades:", places)
            msg = ", ".join(
                s for s in (str(p) for p in places) if s.lower() not in self.false_loc
            )

        print("TENTANDO: " + msg)
        report = try_city(msg, self.apikey, self.lang)

        if isinstance(report, str):
            print(report)
            self.mastodon.status_post(
                f"Oi @{acct}, {report}", in_reply_to_id=status, visibility=visibility
            )
        else:
            print(f"Erro {report}")
            if report == 400:
                self.mastodon.status_post(
                    f"Foi mal @{acct}, não entendi sua mensagem :(",
                    in_reply_to_id=status,
                    visibility=visibility,
                )
            elif report == 401:
                self.mastodon.status_post(
                    f"Foi mal @{acct}, não estou conseguindo saber o clima. Pode dar uma ajuda aqui, @cadu@bolha.one ?",
                    in_reply_to_id=status,
                    visibility=visibility,
                )
            elif report == 404:
                self.mastodon.status_post(
                    f"Foi mal @{acct}, não encontrei a cidade mencionada :(",
                    in_reply_to_id=status,
                    visibility=visibility,
                )
            elif report == 429:
                self.mastodon.status_post(
                    f"Foi mal @{acct}, estou sobrecarregado. Pergunte mais tarde, ok? ;)",
                    in_reply_to_id=status,
                    visibility=visibility,
                )
            else:
                self.mastodon.status_post(
                    f"Parece que você encontrou uma falha, @{acct} ! "
                    f"@cadu@bolha.one e @nandavereda@ayom.media tentarão resolver ;)",
                    in_reply_to_id=status,
                    visibility=visibility,
                )


def main():
    mastodon = Mastodon(
        access_token=os.getenv("MASTODON_TOKEN"),
        api_base_url=os.getenv("MASTODON_BASE_URL"),
    )

    mastodon.account_update_credentials(note=os.getenv("MASTODON_BIO_ONLINE"))
    print("O bot está em funcionamento.")
    try:
        mastodon.stream_user(listener=StreamListenerWeather(mastodon))
    except KeyboardInterrupt:
        print("Interrupção recebida, saindo...")
        mastodon.account_update_credentials(note=os.getenv("MASTODON_BIO_OFFLINE"))
        print("O bot foi encerrado com sucesso.")


if __name__ == "__main__":
    load_dotenv()
    main()
