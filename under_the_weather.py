#!/usr/bin/python3

import os
from lxml import etree
from mastodon import Mastodon, StreamListener
from dotenv import load_dotenv
from openweathermap import try_city


class StreamListenerWeather(StreamListener):
    def __init__(self, mastodon: Mastodon):
        self.apikey = os.getenv('OWM_API')

        self.mastodon = mastodon
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

        content = status.get("content")
        if content is None:
            print("O status estava vazio.")
            return

        print("A mensagem é: " + content)
        # example content (line break added for readability):
        # <p><a href="https://bolha.one/@cadusilva" class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@cadusilva</a>
        # <span> </span>
        # <a href="https://bolha.one/@clima" class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@clima</a>
        # <span> São Paulo</span></p>

        content = etree.XML(content).xpath("string()")

        msg = " ".join((w for w in content.split() if not w.startswith("@")))

        if not msg:
            self.mastodon.status_post(f"@{acct} qual é? Qual foi? Por que é que tu tá nessa?", in_reply_to_id=status)
            return

        print("TENTANDO: " + msg)
        report = try_city(msg, self.apikey)

        if report:
            print(report)
            self.mastodon.status_post(f"@{acct} {report}", in_reply_to_id=status)
        else:
            print("Erro 404")  # report was None
            self.mastodon.status_post(
                f"Foi mal @{acct}, não encontrei a cidade mencionada :(", in_reply_to_id=status
            )


def main():
    mastodon = Mastodon(
        access_token = os.getenv('MASTODON_TOKEN'),
        api_base_url = os.getenv('MASTODON_BASE_URL')
    )

    mastodon.account_update_credentials(note= os.getenv('MASTODON_BIO_ONLINE') )
    print("O bot está em funcionamento.")
    try:
        mastodon.stream_user(listener=StreamListenerWeather(mastodon))
    except KeyboardInterrupt:
        print("Interrupção recebida, saindo...")
        mastodon.account_update_credentials(note= os.getenv('MASTODON_BIO_OFFLINE') )
        print("O bot foi encerrado com sucesso.")


if __name__ == "__main__":
    main()
