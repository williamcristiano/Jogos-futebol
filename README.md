# Jogos-futebol

Este projeto é um script em Python que consulta a "The Odds API" para listar jogos de futebol futuros e suas respectivas odds (cotações) de apostas.

O script busca ligas de futebol, filtra os jogos e salva as informações (Liga, Data, Times, Bookmaker e Odds) em um arquivo CSV chamado `Jogos_raspados.csv`.

## Pré-requisitos

*   Python 3.x
*   Uma chave de API gratuita do The Odds API.

## Instalação

1.  Instale as dependências necessárias:
    ```bash
    pip install requests python-dotenv pandas
    ```

2.  Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API:
    ```env
    API_KEY=sua_chave_aqui
    ```

## Uso

Execute o script principal:

```bash
python main.py
```

O arquivo `Jogos_raspados.csv` será gerado na pasta do projeto.
