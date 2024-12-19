class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.current_room = None

    def move(self, direction):
        if direction in self.current_room.connections:
            self.current_room = self.current_room.connections[direction]
            return f"You move {direction}."
        return "You can't go that way."

    def take_item(self, item_name):
        for item in self.current_room.items:
            if item.name.lower() == item_name.lower() and item.is_collectible:
                self.inventory.append(item)
                self.current_room.items.remove(item)
                return f"You take the {item.name}."
        return "You can't take that."

    def use_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower() and item.is_usable:
                result = item.use(self)
                if result:
                    self.inventory.remove(item)
                return result
        return "You don't have that item."

    def get_inventory_description(self):
        if not self.inventory:
            return "Your inventory is empty."
        return "Inventory: " + ", ".join(item.name for item in self.inventory)

class Room:
    def __init__(self, room_id, name, description):
        self.room_id = room_id
        self.name = name
        self.description = description
        self.items = []
        self.puzzles = []
        self.connections = {}
        self.is_solved = False

    def add_connection(self, direction, room):
        self.connections[direction] = room

    def get_full_description(self):
        desc = f"\n{self.name}\n{self.description}\n"
        if self.items:
            desc += "\nItems here: " + ", ".join(item.name for item in self.items)
        if self.connections:
            desc += "\nExits: " + ", ".join(self.connections.keys())
        return desc

class Item:
    def __init__(self, item_id, name, description):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.is_collectible = True
        self.is_usable = True

    def use(self, player):
        return f"You use the {self.name}."

class Puzzle:
    def __init__(self, puzzle_id, name, description, solution):
        self.puzzle_id = puzzle_id
        self.name = name
        self.description = description
        self.solution = solution
        self.is_solved = False

    def check_solution(self, attempt):
        if attempt.lower() == self.solution.lower():
            self.is_solved = True
            return True
        return False

class GameManager:
    def __init__(self):
        self.player = None
        self.current_room = None
        self.rooms = {}
        self.game_over = False

    def create_game_world(self):
        # Create rooms
        entrance = Room(1, "Entrance Hall", "A dimly lit hall with ancient tapestries.")
        library = Room(2, "Library", "Dusty bookshelves line the walls.")
        lab = Room(3, "Laboratory", "Strange equipment and vials fill the room.")

        # Create connections
        entrance.add_connection("north", library)
        library.add_connection("south", entrance)
        library.add_connection("east", lab)
        lab.add_connection("west", library)

        # Add items
        key = Item(1, "Rusty Key", "An old key that might still work.")
        book = Item(2, "Spellbook", "A book containing magical knowledge.")
        potion = Item(3, "Health Potion", "Restores health when consumed.")

        entrance.items.append(key)
        library.items.append(book)
        lab.items.append(potion)

        # Store rooms
        self.rooms = {
            1: entrance,
            2: library,
            3: lab
        }

    def start_game(self, player_name):
        self.player = Player(player_name)
        self.current_room = self.rooms[1]  # Start at entrance
        self.player.current_room = self.current_room

    def process_command(self, command):
        words = command.lower().split()
        if not words:
            return "Please enter a command."

        action = words[0]
        if len(words) > 1:
            target = " ".join(words[1:])
        else:
            target = ""

        if action == "move":
            return self.player.move(target)
        elif action == "take":
            return self.player.take_item(target)
        elif action == "use":
            return self.player.use_item(target)
        elif action == "look":
            return self.current_room.get_full_description()
        elif action == "inventory":
            return self.player.get_inventory_description()
        else:
            return "Invalid command."
