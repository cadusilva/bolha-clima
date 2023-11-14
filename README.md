# Bolha Clima

O **Bolha Clima** é um robozinho do Mastodon que responde com o clima atual para a cidade informada. Basta citar o bot com o nome da cidade que deseja saber a temperatura, como está o céu e a umidade do ar.

Você pode experimentar em: https://bolha.one/clima

## Como utilizar

Clone o repositório e instale as dependências:

```
pip3 install mastodon.py python-dotenv
```

Agora edite o arquivo `.env`. Veja o que cada linha significa:

- `OWM_API`: API do OpenWeatherMaps. Você pode [usar a sua](https://home.openweathermap.org/api_keys) ou deixar a API do tier gratuito já inclusa para experimentar.
- `OWM_LANG`: idioma das mensagens retornadas pelo OpenWeatherMaps, como "céu limpo" ou "nuvem espaçadas".
- `MASTODON_TOKEN`: token que permite o acesso do robozinho na conta onde ele será usado. Você pode [gerar um token aqui](https://token.bolha.one/?scopes=read+write), preenchendo os campos 1 e 3.
- `MASTODON_BASE_URL`: a URL da instância onde fica a conta que será usada pelo robozinho. Exemplo: `https://bolha.one`
- `MASTODON_BIO_ONLINE`: texto que vai aparecer na bio do bot quando o robozinho estiver em funcionamento.
- `MASTODON_BIO_OFFLINE`: texto que vai aparecer na bio do bot quando o robozinho não estiver sendo executado.

## Origem

O **Bolha Clima** é baseado no [UnderTheWeather](https://github.com/ninedotnine/under_the_weather), abandonado desde 2018, mas ressuscitado e atualizado por [Fernanda Queiroz](https://github.com/nandavereda/under_the_weather).