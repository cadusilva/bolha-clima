# Bolha Clima

O **Bolha Clima** é um robozinho escrito em Python para Mastodon que responde com o clima atual para a cidade informada. Uma vez instalado, basta você citar o bot mencionando somente o nome da cidade e receberá como resposta:

- a temperatura
- a sensação térmica
- o índice UV
- como está o céu, se está encoberto
- a umidade do ar
- o índice UV
- um link para localizar a cidade no mapa

Os dados são fornecidos pelo serviço **WeatherAPI** com base em estações meteorológicas de aeroportos. Você precisa [obter uma chave de API](https://www.weatherapi.com/my/), que é gratuita e permite 1 milhão de consultas por mês.

Experimente o bot em funcionamento aqui: https://bolha.one/@clima

## Como utilizar

Clone o repositório e instale as dependências:

``` bash
git clone https://github.com/cadusilva/bolha-clima.git
pip3 install lxml mastodon.py python-dotenv spacy
python3 -m spacy download pt_core_news_md
```

Crie uma conta em qualquer instância do Mastodon para o bot usar, renomeie `.env.example` para `.env` e edite o arquivo. Veja o que cada linha significa:

- `WTH_API`: API obtida no serviço VisualCrossing. Por padrão, vem vazio. Você precisa gerar e especificar a sua própria chave.

- `WTH_LANG`: idioma das mensagens retornadas pelo VisualCrossing, como "céu limpo" ou "nublado". Veja a lista com os [idiomas disponíveis](https://www.weatherapi.com/docs/#intro-request). Por padrão, vem o idioma português (`pt`).

- `MASTODON_TOKEN`: token necessário para que o robô use a conta destinada a ele. Após logar na instância com a conta do bot, você pode [gerar um token aqui](https://token.bolha.one/?scopes=read+write), preenchendo os campos 1 e 3. Por padrão, o campo vem vazio no `.env`. Você precisa gerar e especificar seu próprio token.

- `MASTODON_BASE_URL`: a URL da instância onde fica a conta que será usada pelo robozinho incluindo `https://` no início, mas sem barra no final. Por padrão, vem vazio. Você precisa especificar sua URL como no exemplo: `https://bolha.one`.

- `MASTODON_BIO_ONLINE`: texto que vai aparecer na bio do bot quando o robozinho estiver em funcionamento.

- `MASTODON_BIO_OFFLINE`: texto que vai aparecer na bio do bot quando o robozinho não estiver sendo executado.

- `UTW_NER_MODEL`: nome do modelo de [NER](https://wikiless.bolha.one/wiki/Named-entity_recognition) usado pela [biblioteca spacy](https://spacy.io/). Por padrão, vem `pt_core_news_md`. Mude apenas se souber o que está fazendo.

- `MAINTENANCE_STATUS`: se esta linha não estiver comentada, ativa o modo de manutenção. Use `{}` na mensagem como referência ao usuário interlocutor.

- `API_TIMEOUT`: até quantos segundos o bot deve esperar por uma resposta da API. Caso ele expire, é retornado o erro `429` e o usuário é informado que o bot está sobrecarregado. Por padrão, são 15 segundos.

Lembre-se de editar as linhas [a partir da 99](https://github.com/cadusilva/bolha-clima/blob/f1554702554bb9ab922727beaa6cbc5ab1bd7422/under_the_weather.py#L99-L119) para definir os perfis que serão notificados em caso de erros.

Para executar o bot, digite:

``` python
python3 under_the_weather.py
```

Agora basta falar com ele através de alguma plataforma do fediverso (Mastodon, Firefish, GoToSocial, etc). Exemplo:

```
Diz aí, @climabot@instancia.xyz, como está o clima no Recife?
```

A resposta será algo assim:

```
Esse é o clima atual em Recife (Pernambuco, Brazil):

- Temperatura: 26 °C
- Sensação térmica: 28 °C
- Céu agora: encoberto, 75% encoberto
- Umidade do ar: 89%
- Índice UV: 9 de 11

🕒 Atualizado às 09:00 (horário local)
🗺️ Ver no mapa: https://www.openstreetmap.org/?mlat=-8.05&mlon=-34.9
ℹ️ Com informações de WeatherAPI
```

> A **WeatherAPI** não lida muito bem com acentuação do idioma português. Por isso, `João Pessoa` pode retornar `Pessoa, AL`. Nesse caso, tire a acentuação que o resultado deve vir corretamente.

## Usando sem robô

Você também pode consultar o clima atual de qualquer cidade sem precisar instalar o bot em uma instância. Basta usar o seguinte comando:

``` python
python3 openweathermap.py "Nome da Cidade"
```

Se o nome for simples, como `Recife`, não precisa de aspas. Mas se for composto, como `Rio de Janeiro`, use as aspas. O script então retornará as informações do jeito que ele postaria no perfil do robô, conforme exemplo acima.

## Serviço do `systemd`

Para rodar o bot como um serviço do sistema, use o seguinte exemplo:

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

Neste modo o robô não consulta a API e simplesmente responde dizendo que está indisponível no momento. Para ativar, descomente a linha `MAINTENANCE_STATUS` no arquivo `.env` e personalize a mensagem que será enviada ao usuário. Onde você colocar `{}` será onde irá aparecer o @ da pessoa a quem se está respondendo.

Para desativar o modo manutenção, comente a linha que começa com `MAINTENANCE_STATUS` e reinicie o bot.

## Créditos

O **Bolha Clima** é baseado no [UnderTheWeather](https://github.com/ninedotnine/under_the_weather), abandonado desde 2018, mas ressuscitado e atualizado por [Fernanda Queiroz](https://github.com/nandavereda/under_the_weather). O autor original não planeja dar continuidade ao projeto, mas ele seguirá vivo neste repositório.

O bot está licenciado sob a AGPL. Vide arquivo `LICENSE` para conhecer o conteúdo da licença na íntegra.