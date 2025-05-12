import random
import uuid


class Player:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.position = 1

    def __str__(self):
        return f"{self.name} @ {self.position}"


class Board:
    def __init__(self, size=100, snakes=None, ladders=None):
        self.size = size
        self.snakes = snakes or {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = ladders or {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

    def get_next_position(self, pos):
        if pos in self.snakes:
            print(f"🐍 Snake from {pos} to {self.snakes[pos]}")
            return self.snakes[pos]
        elif pos in self.ladders:
            print(f"🪜 Ladder from {pos} to {self.ladders[pos]}")
            return self.ladders[pos]
        return pos


class SnakeAndLadderGame:
    def __init__(self, players, board=None):
        self.players = players
        self.board = board or Board()
        self.current_turn = 0
        self.winner = None

    def roll_dice(self):
        return random.randint(1, 6)

    def play_turn(self):
        if self.winner:
            print(f"🎉 Game already won by {self.winner.name}")
            return

        player = self.players[self.current_turn]
        roll = self.roll_dice()
        print(f"{player.name} rolled a 🎲 {roll}")
        new_pos = player.position + roll
        if new_pos > self.board.size:
            print(f"{player.name} stays at {player.position}")
        else:
            player.position = self.board.get_next_position(new_pos)
            print(f"{player.name} moved to {player.position}")
            if player.position == self.board.size:
                self.winner = player
                print(f"🎉 {player.name} has won the game!")

        self.current_turn = (self.current_turn + 1) % len(self.players)


class GameSessionManager:
    def __init__(self):
        self.sessions = {}  # session_id -> SnakeAndLadderGame

    def create_game(self, player_names):
        players = [Player(name) for name in player_names]
        game = SnakeAndLadderGame(players)
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = game
        return session_id

    def get_game(self, session_id):
        return self.sessions.get(session_id)
