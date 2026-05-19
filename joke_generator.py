"""
Random Joke Generator using External APIs
A simple utility to fetch random jokes from various sources
"""

import requests
import json
from typing import Dict, Optional


class JokeGenerator:
    """Fetch random jokes from external APIs"""
    
    # Available joke APIs
    JOKE_APIS = {
        'jokes_api': 'https://v2.jokeapi.dev/joke/Any',
        'dad_jokes': 'https://icanhazdadjoke.com/',
        'random_user_joke': 'https://api.api-ninjas.com/v1/jokes'
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TipsyBot/1.0 (Community Bot)'
        })
    
    def get_joke_from_jokeapi(self) -> Optional[Dict]:
        """
        Fetch joke from JokeAPI (v2.jokeapi.dev)
        Supports programming, knock-knock, general jokes
        """
        try:
            response = self.session.get(
                self.JOKE_APIS['jokes_api'],
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('type') == 'twopart':
                return {
                    'source': 'JokeAPI',
                    'setup': data.get('setup'),
                    'delivery': data.get('delivery'),
                    'category': data.get('category')
                }
            else:
                return {
                    'source': 'JokeAPI',
                    'joke': data.get('joke'),
                    'category': data.get('category')
                }
        except requests.RequestException as e:
            print(f"Error fetching from JokeAPI: {e}")
            return None
    
    def get_dad_joke(self) -> Optional[Dict]:
        """
        Fetch dad joke from icanhazdadjoke.com
        Classic dad jokes API
        """
        try:
            response = self.session.get(
                self.JOKE_APIS['dad_jokes'],
                headers={'Accept': 'application/json'},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'source': 'Dad Jokes',
                'joke': data.get('joke'),
                'id': data.get('id')
            }
        except requests.RequestException as e:
            print(f"Error fetching Dad Joke: {e}")
            return None
    
    def get_random_joke(self, api_source: str = 'random') -> Optional[Dict]:
        """
        Get a random joke from available APIs
        
        Args:
            api_source: 'jokeapi', 'dadjoke', or 'random' for random selection
        
        Returns:
            Dictionary with joke data or None on failure
        """
        import random
        
        if api_source == 'random':
            api_source = random.choice(['jokeapi', 'dadjoke'])
        
        if api_source.lower() == 'jokeapi':
            return self.get_joke_from_jokeapi()
        elif api_source.lower() == 'dadjoke':
            return self.get_dad_joke()
        else:
            print(f"Unknown API source: {api_source}")
            return None
    
    def format_joke(self, joke_data: Dict) -> str:
        """Format joke data into readable string"""
        if not joke_data:
            return "Could not fetch a joke. Please try again!"
        
        source = joke_data.get('source', 'Unknown')
        
        if 'setup' in joke_data:
            # Two-part joke
            return f"{joke_data['setup']}\n\n{joke_data['delivery']}\n\n_(Source: {source})_"
        elif 'joke' in joke_data:
            # Single-part joke
            return f"{joke_data['joke']}\n\n_(Source: {source})_"
        else:
            return "Invalid joke format"


def main():
    """Example usage of JokeGenerator"""
    generator = JokeGenerator()
    
    print("🎭 Random Joke Generator 🎭\n")
    
    # Get a random joke
    joke = generator.get_random_joke()
    if joke:
        print(generator.format_joke(joke))
    
    print("\n" + "="*50 + "\n")
    
    # Get a specific joke from JokeAPI
    print("Getting joke from JokeAPI...\n")
    joke = generator.get_joke_from_jokeapi()
    if joke:
        print(generator.format_joke(joke))
    
    print("\n" + "="*50 + "\n")
    
    # Get a Dad Joke
    print("Getting Dad Joke...\n")
    joke = generator.get_dad_joke()
    if joke:
        print(generator.format_joke(joke))


if __name__ == "__main__":
    main()
