# app.py
from flask import Flask, render_template, request, jsonify, session
from game_logic import GameManager, Player, Room, Item, Puzzle

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session management

# Initialize game state
game_state = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global game_state
    game_state = GameState()
    player_name = request.json.get('player_name')
    game_state.game_manager.start_game(player_name)
    return jsonify({
        'message': 'Game started',
        'room_description': game_state.game_manager.current_room.get_full_description()
    })

@app.route('/process_command', methods=['POST'])
def process_command():
    global game_state
    if not game_state:
        return jsonify({'error': 'Game not started'})
    
    command = request.json.get('command')
    result = game_state.game_manager.process_command(command)
    
    response = {
        'message': result,
        'room_description': game_state.game_manager.current_room.get_full_description(),
        'inventory': game_state.game_manager.player.get_inventory_description(),
        'health': game_state.game_manager.player.health,
        'game_over': game_state.game_manager.game_over
    }
    
    return jsonify(response)

# The GameState class definition can stay the same
class GameState:
    def __init__(self):
        self.game_manager = GameManager()
        self.game_manager.create_game_world()

# This is important for Vercel
app.debug = False

# Required for Vercel
if __name__ == '__main__':
    app.run()
