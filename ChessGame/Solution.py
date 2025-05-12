from abc import ABC, abstractmethod


class Position:
    def __init__(self, x, y):
        self.x = x  # Row
        self.y = y  # Column

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x},{self.y})"


class Piece(ABC):
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position
        self.has_moved = False

    @abstractmethod
    def is_valid_move(self, board, dest):
        pass

    def move(self, dest):
        self.position = dest
        self.has_moved = True


class King(Piece):
    def is_valid_move(self, board, dest):
        dx = abs(dest.x - self.position.x)
        dy = abs(dest.y - self.position.y)
        return dx <= 1 and dy <= 1


class Queen(Piece):
    def is_valid_move(self, board, dest):
        dx = abs(dest.x - self.position.x)
        dy = abs(dest.y - self.position.y)
        return dx == dy or dx == 0 or dy == 0


class Rook(Piece):
    def is_valid_move(self, board, dest):
        return self.position.x == dest.x or self.position.y == dest.y


class Bishop(Piece):
    def is_valid_move(self, board, dest):
        return abs(dest.x - self.position.x) == abs(dest.y - self.position.y)


class Knight(Piece):
    def is_valid_move(self, board, dest):
        dx = abs(dest.x - self.position.x)
        dy = abs(dest.y - self.position.y)
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)


class Pawn(Piece):
    def is_valid_move(self, board, dest):
        direction = 1 if self.color == 'white' else -1
        dx = dest.x - self.position.x
        dy = abs(dest.y - self.position.y)
        is_forward = dx == direction and dy == 0 and board.is_empty(dest)
        is_capture = dx == direction and dy == 1 and not board.is_empty(dest)
        return is_forward or is_capture


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        for color, row_pawn, row_other in [('white', 6, 7), ('black', 1, 0)]:
            pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
            for i in range(8):
                self.grid[row_pawn][i] = Pawn(color, Position(row_pawn, i))
                self.grid[row_other][i] = pieces[i](color, Position(row_other, i))

    def get_piece(self, pos):
        return self.grid[pos.x][pos.y]

    def move_piece(self, src, dest):
        piece = self.get_piece(src)
        self.grid[dest.x][dest.y] = piece
        self.grid[src.x][src.y] = None
        piece.move(dest)

    def is_empty(self, pos):
        return self.get_piece(pos) is None

    def is_valid_position(self, pos):
        return 0 <= pos.x < 8 and 0 <= pos.y < 8

    def find_king(self, color):
        for row in self.grid:
            for piece in row:
                if isinstance(piece, King) and piece and piece.color == color:
                    return piece.position
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        for row in self.grid:
            for piece in row:
                if piece and piece.color != color and piece.is_valid_move(self, king_pos):
                    return True
        return False
