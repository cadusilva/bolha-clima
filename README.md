# Bolha Clima

O **Bolha Clima** é um robozinho escrito em Python para Mastodon que responde com o clima atual para a cidade informada. Uma vez instalado, basta você citar o bot mencionando somente o nome da cidade e receberá como resposta:

- a temperatura
- a sensação térmica
- como está o céu, se está encoberto
- a umidade do ar
- um link para localizar a cidade no mapa

Os dados são fornecidos pelo serviço [VisualCrossinng](https://www.visualcrossing.com/).

> O link que mostra no mapa a localização da cidade consultada não se refere a sua posição precisa, apenas um ponto vago dentro do município informado. Primeiro que não é coletada sua geolocalização, nem qualquer dado é armazenado na **Bolha.one**. Mesmo os toots com as respostas são apagados depois de 1 semana.

Experimente o bot em funcionamento aqui: https://bolha.one/@clima

## Como utilizar

Clone o repositório e instale as dependências:

``` bash
git clone https://github.com/cadusilva/bolha-clima.git
pip3 install lxml mastodon.py python-dotenv spacy
python3 -m spacy download pt_core_news_md
```

Crie uma conta em qualquer instância do Mastodon para o bot usar, renomeie `.env.example` para `.env` e edite o arquivo. Veja o que cada linha significa:

- `WTH_API`: informe aqui sua [chave de API](https://www.visualcrossing.com/weather-api) do serviço **VisualCrossing**.
- `WTH_LANG`: defina aqui o [idioma das mensagens](https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/) retornadas pelo VisualCrossing, como "céu limpo" ou "nublado". Por padrão, vem o idioma português (`pt`).
- `MASTODON_TOKEN`: define o token de acesso da conta que será usada pelo robô. Após logar na instância com a conta do bot, você pode [gerar um token aqui](https://token.bolha.one/?scopes=read+write), preenchendo os campos 1 e 3.
- `MASTODON_BASE_URL`: define o URL da instância onde fica a conta que será usada pelo robozinho incluindo `https://` no início, mas sem barra no final. Exemplo: `https://bolha.one`.
- `MASTODON_BIO_ONLINE`: define o texto que vai aparecer na bio do bot quando o robozinho estiver em funcionamento.
- `MASTODON_BIO_OFFLINE`: define o texto que vai aparecer na bio do bot quando o robozinho não estiver sendo executado.
- `UTW_NER_MODEL`: define o nome do modelo de [NER](https://wikiless.bolha.one/wiki/Named-entity_recognition) usado pela [biblioteca spacy](https://spacy.io/). Não altere, a menos que saiba o que está fazendo.
- `MAINTENANCE_STATUS`: ativa e define a mensagem do modo de manutenção, a qual o bot irá usar para responder interações com ele. Para ativar o modo de manutenção, remova o jogo-da-velha (`#`) no início da linha. Use `{}` na mensagem como referência ao usuário interlocutor.
- `API_TIMEOUT`: define o tempo em segundos que o bot deve esperar por uma resposta da API. Caso ele expire, é retornado o erro `429` e o usuário é informado que o bot está sobrecarregado.

> Lembre-se de editar as linhas [a partir da 99](https://github.com/cadusilva/bolha-clima/blob/f1554702554bb9ab922727beaa6cbc5ab1bd7422/under_the_weather.py#L99-L119) para definir os perfis que serão notificados em caso de erros.

Depois de definir os parâmetros acima no arquivo `.env`, execute o bot digitando:

``` python
python3 under_the_weather.py
```

Agora basta falar com ele através de alguma plataforma do fediverso (Mastodon, Firefish, GoToSocial, etc). Exemplo:

```
@climabot@instancia.xyz como está o clima no Recife?
```

A resposta será algo assim:

```
O clima em Recife, PE, Brasil às 23h é:

- Temperatura: 29 °C
- Sensação térmica: 33 °C
- Índice UV: 0 de 11
- Céu agora: parcialmente nublado, 88% encoberto, 0% de chances de chuva
- Umidade do ar: 70%

📅 Para amanhã, a temperatura pode alcançar 28 °C com sensação térmica de até 32 °C e 52% de chances de chover.

📍 Ver cidade no mapa: https://www.openstreetmap.org/?mlat=-8.05603&mlon=-34.8704
ℹ️ Com informações de VisualCrossing
⌚ O horário mencionado é o da cidade pesquisada.
```

## Usando com Docker

Você pode rodar seu robozinho do clima dentro de um contêiner **Docker** facilmente. Não precisa editar o arquivo `.env` pois você vai editar o arquivo `docker-compose.yml` e definir nele os parâmetros das variáveis de ambiente conforme explicado acima. Depois execute:

``` bash
docker-compose up -d
```

## Usando sem robô

Você também pode consultar o clima atual de qualquer cidade sem precisar instalar o bot em uma instância. Basta usar o seguinte comando:

``` python
python3 openweathermap.py "Nome da Cidade"
```

Se o nome for simples, como `Recife`, não precisa de aspas. Mas se for composto, como `Rio de Janeiro`, use as aspas. O script então retornará as informações do jeito que ele postaria no perfil do robô, conforme exemplo acima.

## Serviço do `systemd`

Para rodar o bot como um serviço do sistema Linux, use o seguinte exemplo:

``` ini
[Unit]
Description=Bot Bolha Clima
After=network-online.target

[Service]
Type=simple
DynamicUser=yes
Restart=on-failure
RestartSec=1
WorkingDirectory=/opt/clima
ExecStart=/usr/bin/python3 /opt/clima/under_the_weather.py
KillSignal=SIGINT
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

Lembre-se de alterar o caminho `/opt/clima` caso tenha clonado os arquivos em outro lugar e o nome do seu bot na linha `Description`. Para iniciar o serviço e fazer ele carregar junto com o sistema, execute:

``` bash
systemctl daemon-reload
systemctl enable --now clima
```

Em caso de problemas, execute um dos dois comandos abaixo para ler os logs de funcionamento:

``` bash
systemctl status clima
journalctl -u clima [--follow]
```

## Modo de Manutenção

Neste modo o robô não consulta a API e simplesmente responde o usuário dizendo que está indisponível no momento. Para ativar, descomente a linha `MAINTENANCE_STATUS` no arquivo `.env` (ou no `docker-compose.yml`, caso esteja usando Docker) e personalize a mensagem que será enviada ao usuário.

Onde você colocar `{}` será onde irá aparecer o @ da pessoa a quem se está respondendo. Para desativar o modo manutenção, comente a linha que começa com `MAINTENANCE_STATUS` e reinicie o bot.

## Créditos

O **Bolha Clima** é baseado no [UnderTheWeather](https://github.com/ninedotnine/under_the_weather), abandonado desde 2018, mas ressuscitado e atualizado por [Fernanda Queiroz](https://github.com/nandavereda/under_the_weather). O autor original não planeja dar continuidade ao projeto, mas ele seguirá vivo neste repositório.

O bot está licenciado sob a AGPL. Vide arquivo `LICENSE` para conhecer o conteúdo da licença na íntegra.