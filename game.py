# app.py
from flask import Flask, jsonify, request, render_template
from game import Room, Player, create_game_world

app = Flask(__name__)

# Initialize game state
player = Player("Mysterious Adventurer")
player.current_room = create_game_world()

@app.route('/')
def index():
    return render_template('report.html')

@app.route('/game-state', methods=['GET'])
def game_state():
    return jsonify({
        'current_room': player.current_room.name,
        'description': player.current_room.description,
        'items': player.current_room.items,
        'inventory': player.inventory,
        'links': list(player.current_room.links.keys()),
        'puzzles': list(player.current_room.puzzles.keys())
    })

@app.route('/action', methods=['POST'])
def action():
    data = request.json
    command = data.get('command')
    response = {'success': False, 'message': ''}

    if command.startswith("move"):
        _, direction = command.split()
        if direction in player.current_room.links:
            player.current_room = player.current_room.links[direction]
            response['success'] = True
            response['message'] = f"Moved to {player.current_room.name}."
        else:
            response['message'] = "You can't go that way!"

    elif command.startswith("pick"):
        _, item = command.split()
        if item in player.current_room.items:
            player.inventory.append(item)
            player.current_room.items.remove(item)
            response['success'] = True
            response['message'] = f"{item} added to your inventory."
        else:
            response['message'] = "Item not found in this room."

    elif command.startswith("solve"):
        _, puzzle = command.split()
        solution = data.get('solution')
        if puzzle in player.current_room.puzzles:
            if solution == player.current_room.puzzles[puzzle]:
                player.solved_puzzles.append(puzzle)
                response['success'] = True
                response['message'] = "Puzzle solved!"
            else:
                response['message'] = "Incorrect solution."
        else:
            response['message'] = "No such puzzle here."

    elif command == "inventory":
        response['success'] = True
        response['message'] = f"Inventory: {', '.join(player.inventory) if player.inventory else 'Empty'}"

    else:
        response['message'] = "Invalid command!"

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
