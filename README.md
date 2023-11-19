# Bolha Clima

O **Bolha Clima** é um robozinho escrito em Python para Mastodon que responde com o clima atual para a cidade informada. Uma vez instalado, basta você citar o bot mencionando somente o nome da cidade e receberá como resposta:

- a temperatura
- a sensação térmica
- o índice UV
- como está o céu, se está encoberto
- a umidade do ar
- as chances de chover
- a previsão para o dia seguinte

Os dados são fornecidos pelo serviço **VisualCrossing** com base em estações meteorológicas de aeroportos. Você precisa [obter uma chave de API](https://www.visualcrossing.com/sign-up), que é gratuita e permite 1.000 consultas por dia.

Experimente o bot em funcionamento aqui: https://bolha.one/@clima

## Como utilizar

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/cadusilva/bolha-clima.git
pip3 install lxml mastodon.py python-dotenv spacy
python3 -m spacy download pt_core_news_md
```

Crie uma conta em qualquer instância do Mastodon para o bot usar, renomeie `.env.example` para `.env` e edite o arquivo. Veja o que cada linha significa:

- `WTH_API`: API obtida no serviço VisualCrossing.
- `WTH_LANG`: idioma das mensagens retornadas pelo VisualCrossing, como "céu limpo" ou "nublado".
- `MASTODON_TOKEN`: token necessário para que o robô use a conta destinada a ele. Após logar na instância com a conta do bot, você pode [gerar um token aqui](https://token.bolha.one/?scopes=read+write), preenchendo os campos 1 e 3.
- `MASTODON_BASE_URL`: a URL da instância onde fica a conta que será usada pelo robozinho incluindo `https://` no início, mas sem barra no final. Exemplo: `https://bolha.one`
- `MASTODON_BIO_ONLINE`: texto que vai aparecer na bio do bot quando o robozinho estiver em funcionamento.
- `MASTODON_BIO_OFFLINE`: texto que vai aparecer na bio do bot quando o robozinho não estiver sendo executado.
- `UTW_NER_MODEL`: nome do modelo de [NER](https://wikiless.bolha.one/wiki/Named-entity_recognition) usado pela [biblioteca spacy](https://spacy.io/)

Lembre-se de editar as linhas [a partir da 99](https://github.com/cadusilva/bolha-clima/blob/f1554702554bb9ab922727beaa6cbc5ab1bd7422/under_the_weather.py#L99-L119) para definir os perfis que serão notificados em caso de erros.

Para executar o bot, digite:

```python
python3 under_the_weather.py
```

Agora basta falar com ele. Exemplo:

```
Diz aí, @climabot@instancia.xyz, como está o clima no Recife?
```

A resposta será algo assim:

```
Esse é o clima em Recife, PE, Brasil às 22:00 (horário local):

- Temperatura: 27 °C (sensação de 30 °C)
- Céu agora: parcialmente nublado, 50% encoberto
- Índice UV: 0 de 10
- Umidade do ar: ~79%
- Chances de chover hoje: ~100%

- A previsão para amanhã é 30 °C de máxima, mínima de 27 °C e sensação de até 34 °C, com céu parcialmente nublado ao longo do dia com uma chance de chuva ao longo do dia. Há 10% de chances de clima severo, como tempestades.
```

Caso o nome da cidade informada seja o mesmo em diferentes estados, você pode especificar a `UF` do estado desejado para ter o resultado esperado. Exemplo:

```
@climabot@instancia.xyz Ipapeva, MG
@climabot@instancia.xyz Ipapeva, SP
```

O bot tenta adivinhar a cidade certa mesmo que você não informe a UF mas, caso ele retorne o município errado, você pode especificar o estado onde fica o município esperado. Para ter respostas mais precisas, prefira sempre especificar na consulta a UF do estado onde fica a cidade desejada.

## Usando sem robô

Você também pode consultar o clima atual de qualquer cidade sem precisar instalar o bot em uma instância. Basta usar o seguinte comando:

```python
python3 openweathermap.py "Nome da Cidade"
```

Se o nome for simples, como `Recife`, não precisa de aspas. Mas se for composto, como `Rio de Janeiro`, use as aspas. O script então retornará as informações do jeito que ele postaria no perfil do robô, conforme exemplo acima.

## Serviço do `systemd`

Para rodar o bot como um serviço do sistema, use o seguinte exemplo:

```ini
cat << EOF > /etc/systemd/system/clima.service
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
EOF
```

Lembre-se de alterar o caminho `/opt/clima` caso tenha clonado os arquivos em outro lugar e o nome do seu bot na linha `Description`. Para iniciar o serviço e fazer ele carregar junto com o sistema, execute:

```bash
systemctl daemon-reload
systemctl enable --now clima
```

Em caso de problemas, execute um dos dois comandos abaixo para ler os logs de funcionamento:

```bash
systemctl status clima
journalctl -u clima
```

## Créditos

O **Bolha Clima** é baseado no [UnderTheWeather](https://github.com/ninedotnine/under_the_weather), abandonado desde 2018, mas ressuscitado e atualizado por [Fernanda Queiroz](https://github.com/nandavereda/under_the_weather). O autor original não planeja dar continuidade ao projeto, mas ele seguirá vivo neste repositório.

O bot está licenciado sob a AGPL. Vide arquivo `LICENSE` para conhecer o conteúdo da licença na íntegra.