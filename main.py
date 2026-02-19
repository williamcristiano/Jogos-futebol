import requests
from dotenv import load_dotenv
import os
import pandas
from typing import List, Dict, Any, Optional

load_dotenv()
class API:
    def __init__(self):
        """Inicializa a classe API carregando a chave de API."""
        self.API_KEY = os.getenv("API_KEY")
        self.orquestrador()

    def orquestrador(self) -> None:
        """Gerencia o fluxo de obtenção de dados e criação do arquivo."""
        data = self.get_all_sports()
        all_matches = []
        if data:
            soccer_data = [sport for sport in data if sport.get('group') == 'Soccer']
    
            for sport in soccer_data:
                print(f"Buscando odds para: {sport['title']}")
                odds_data = self.get_odds(sport['key'])
                
                if odds_data:
                    for game in odds_data:
                        row = {
                            'League': sport['title'],
                            'Date': game['commence_time'],
                            'Home Team': game['home_team'],
                            'Away Team': game['away_team']
                        }
                        
                        if game.get('bookmakers'):
                            bookmaker = game['bookmakers'][0]
                            row['Bookmaker'] = bookmaker['title']
                            for market in bookmaker.get('markets', []):
                                if market['key'] == 'h2h': 
                                    for outcome in market['outcomes']:
                                        if outcome['name'] == game['home_team']:
                                            row['Home Odd'] = outcome['price']
                                        elif outcome['name'] == game['away_team']:
                                            row['Away Odd'] = outcome['price']
                                        elif outcome['name'] == 'Draw':
                                            row['Draw Odd'] = outcome['price']
                        
                        all_matches.append(row)

            self.create_file(all_matches)

    def get_all_sports(self) -> Optional[List[Dict[str, Any]]]:
        """Busca todos os esportes disponíveis na API."""
        url = "https://api.the-odds-api.com/v4/sports"
        params = {
            'api_key': self.API_KEY,
        }
        sports_response= requests.get(url,params=params)
        if sports_response.status_code != 200:
            print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
        else:
            return sports_response.json()
        
    def get_odds(self, sport_key: str) -> List[Dict[str, Any]]:
        """Busca as odds para um esporte específico."""
        url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
        params = {
            'api_key': self.API_KEY,
            'regions': 'eu',
            'markets': 'h2h',
            'oddsFormat': 'decimal'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get odds for {sport_key}: {response.status_code}")
            return []

    def create_file(self, data: List[Dict[str, Any]]) -> None:
        """Cria um arquivo CSV com os dados coletados."""
        df = pandas.DataFrame(data)
        df.to_csv("Jogos_raspados.csv")

if __name__ == "__main__":
    API()
