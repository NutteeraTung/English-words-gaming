import requests
import json

base_url = 'https://api.dictionaryapi.dev/api/v2/entries/en'

def create_word():
    global word_start, word_end, defined_word
    word_start = str(input('The word start with = '))
    print(word_start)
    word_end = str(input('The word end with = '))
    print(word_end)
    defined_word = str(input('Enter the word: '))
    print(defined_word)

create_word()

class StartGame:
    def __init__(self):
        self.word_data = None
    
    def check_english_word(self, word):
        """Check if word exists in the API"""
        url = f'{base_url}/{word}'
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            print('Data retrieved!!')
            self.word_data = response.json()
            item = self.word_data[0]
            print('This word is existing!')
            for meaning in item["meanings"]:
                keys = list(meaning.keys())
                if "definitions" in keys:
                    index = keys.index("definitions")
                    definitions = meaning["definitions"]
                    print(definitions)
            return True
        else:
            print(f'Failed to retrieve data, {response.status_code}')
            return False
    
    def recheck_word(self, defined_word):
        """Validate word start/end and retrieve definition"""
        if word_start == defined_word[0]:
            print('The start word is true')
            if word_end == defined_word[len(defined_word) - 1]:
                print('The end word is true')
                # Call the method on self, not on the string
                result = self.check_english_word(defined_word)
                print(f'Waiting for the results: {result}')
            else:
                print('The end word is not true')
        else:
            print('You are cheating!')

# Create instance and call the method
game = StartGame()
game.recheck_word(defined_word)