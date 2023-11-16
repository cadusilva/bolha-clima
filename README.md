# Bolha Clima

O **Bolha Clima** é um robozinho escrito em Python para Mastodon que responde com o clima atual para a cidade informada. Uma vez instalado, basta você citar o bot mencionando somente o nome da cidade e receberá como resposta:

- a temperatura
- a sensação térmica
- o índice UV
- como está o céu, se está encoberto
- a umidade do ar
- as chances de chover

Os dados são fornecidos pelo serviço **VisualCrossing** com base em estações meteorológicas de aeroportos. Você precisa [obter uma chave de API](https://www.visualcrossing.com/sign-up), que é gratuita e permite 1.000 consultas por dia.

Experimente o bot em funcionamento aqui: https://bolha.one/@clima

## Como utilizar

Clone o repositório e instale as dependências:

```
git clone https://github.com/cadusilva/bolha-clima.git
pip3 install mastodon.py python-dotenv
```

Crie uma conta em qualquer instância do Mastodon para o bot usar, renomeie `.env.example` para `.env` e edite o arquivo. Veja o que cada linha significa:

- `WTH_API`: API obtida no serviço VisualCrossing.
- `WTH_LANG`: idioma das mensagens retornadas pelo VisualCrossing, como "céu limpo", "nublado" ou "nuvem espaçadas".
- `MASTODON_TOKEN`: token necessário para que o robô use a conta destinada a ele. Após logar na instância, você pode [gerar um token aqui](https://token.bolha.one/?scopes=read+write), preenchendo os campos 1 e 3.
- `MASTODON_BASE_URL`: a URL da instância onde fica a conta que será usada pelo robozinho incluindo `https://` no início, mas sem barra no final. Exemplo: `https://bolha.one`
- `MASTODON_BIO_ONLINE`: texto que vai aparecer na bio do bot quando o robozinho estiver em funcionamento.
- `MASTODON_BIO_OFFLINE`: texto que vai aparecer na bio do bot quando o robozinho não estiver sendo executado.

Para executar o bot, digite:

```
python3 under_the_weather.py
```

Agora basta falar com ele. Exemplo:

```
@bot@instancia.xyz Recife
```

A resposta será algo assim:

```
clima em Recife, PE, Brasil às 23h:
- Temperatura: 27.0 °C
- Sensação térmica: 29.5 °C
- Índice UV: 0/10
- Céu agora: Parcialmente nublado, 50% encoberto
- Umidade do ar: ~79%
- Chances de chover: ~0%
```
Lembre-se apenas de editar as linhas [a partir da 99](https://github.com/cadusilva/bolha-clima/blob/f1554702554bb9ab922727beaa6cbc5ab1bd7422/under_the_weather.py#L99-L119) para definir os perfis que serão notificados em caso de erros.

## Usando sem robô

Você também pode consultar o clima atual de qualquer cidade sem depender de um bot. Basta usar o seguinte comando:

```
python3 openweathermap.py "Nome da Cidade"
```

Se o nome for simples, como `Recife`, não precisa de aspas. Mas se for composto, como `Rio de Janeiro`, use as aspas. O script então retornará as informações do jeito que ele postaria no perfil do robô, conforme exemplo acima.

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

Em caso de problemas, execute um dos dois comandos abaixo para ler os logs de funcionamento:

```
systemctl status clima
journalctl -u clima
```

## Créditos

O **Bolha Clima** é baseado no [UnderTheWeather](https://github.com/ninedotnine/under_the_weather), abandonado desde 2018, mas ressuscitado e atualizado por [Fernanda Queiroz](https://github.com/nandavereda/under_the_weather). O autor original não planeja dar continuidade ao projeto, mas ele seguirá vivo neste repositório.