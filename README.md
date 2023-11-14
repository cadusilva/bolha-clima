# Bolha Clima

O **Bolha Clima** é um robozinho do Mastodon escrito em Python que responde com o clima atual para a cidade informada. Basta citar o bot com o nome da cidade que deseja saber a temperatura, como está o céu e a umidade do ar.

Você pode experimentar em: https://bolha.one/@clima

## Como utilizar

Clone o repositório e instale as dependências:

```
pip3 install mastodon.py python-dotenv
```

Crie uma conta em alguma instância do Mastodon para o bot e edite o arquivo `.env`. Veja o que cada linha significa:

- `OWM_API`: API do OpenWeatherMap. Você pode [usar a sua](https://home.openweathermap.org/api_keys) ou deixar a API do tier gratuito já inclusa para experimentar.
- `OWM_LANG`: idioma das mensagens retornadas pelo OpenWeatherMap, como "céu limpo", "nublado" ou "nuvem espaçadas".
- `MASTODON_TOKEN`: token que permite o acesso do robozinho na conta onde ele será usado. Você pode [gerar um token aqui](https://token.bolha.one/?scopes=read+write), preenchendo os campos 1 e 3.
- `MASTODON_BASE_URL`: a URL da instância onde fica a conta que será usada pelo robozinho incluindo `https://` no início, mas sem barra no final. Exemplo: `https://bolha.one`
- `MASTODON_BIO_ONLINE`: texto que vai aparecer na bio do bot quando o robozinho estiver em funcionamento.
- `MASTODON_BIO_OFFLINE`: texto que vai aparecer na bio do bot quando o robozinho não estiver sendo executado.

Para executar o bot, digite:

```
python3 under_the_weather.py
```

Agora basta falar com o bot. Exemplo:

```
@clima@bolha.one Recife
```

A resposta será algo assim:

```
O clima atual em Recife, BR é esse: faz 30 °C com sensação
térmica de 34 °C, nuvens dispersas e umidade do ar em 66%.
```

## Serviço do `systemd`

Para rodar o bot como um serviço do sistema, use o seguinte exemplo:

```
cat << EOF > /etc/systemd/system/clima.service
[Unit]
Description=Bot Bolha Clima
After=network-online.target

[Service]
Type=simple
Environment="PYTHONUNBUFFERED=1"
Restart=on-failure
User=nobody
WorkingDirectory=/opt/clima
ExecStart=/usr/bin/python3 /opt/clima/under_the_weather.py

[Install]
WantedBy=multi-user.target
EOF
```

Lembre-se de alterar o caminho `/opt/clima` caso tenha clonado os arquivos em outro lugar e o nome do seu bot na linha `Description`. Para iniciar o serviço e fazer ele carregar junto com o sistema, execute:

```
# systemctl daemon-reload
# systemctl enable --now clima
```

## Origem

O **Bolha Clima** é baseado no [UnderTheWeather](https://github.com/ninedotnine/under_the_weather), abandonado desde 2018, mas ressuscitado e atualizado por [Fernanda Queiroz](https://github.com/nandavereda/under_the_weather).