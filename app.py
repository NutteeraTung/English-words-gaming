from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en'

class StartGame:
    def __init__(self):
        self.word_data = None

    def check_english_word(self, word):
        """Check if word exists in the API"""
        url = f'{BASE_URL}/{word}'
        response = requests.get(url)
        if response.status_code == 200:
            self.word_data = response.json()
            item = self.word_data[0]
            definitions = []
            for meaning in item.get("meanings", []):
                for definition in meaning.get("definitions", []):
                    definitions.append(definition.get("definition", ""))
            return True, definitions
        return False, []

    def recheck_word(self, word_start, word_end, defined_word):
        """Validate word start/end and retrieve definition"""
        if not defined_word or len(defined_word) < 2:
            return False, "The word is too short."
        
        if word_start.lower() != defined_word[0].lower():
            return False, "Your word does not start with the correct letter."
        
        if word_end.lower() != defined_word[-1].lower():
            return False, "Your word does not end with the correct letter."
        
        valid, meanings = self.check_english_word(defined_word)
        if not valid:
            return False, f'"{defined_word}" is not an English word!'
        
        definition = meanings[0] if meanings else "No definition found, but the word exists!"
        return True, f'Great! "{defined_word}": {definition}'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    w_start = data.get('start', '').strip()
    w_end = data.get('end', '').strip()
    word = data.get('word', '').strip()
    
    game = StartGame()
    ok, message = game.recheck_word(w_start, w_end, word)
    return jsonify({'ok': ok, 'message': message})

if __name__ == '__main__':
    app.run(debug=True)