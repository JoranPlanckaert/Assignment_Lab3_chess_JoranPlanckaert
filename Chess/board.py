import json
from pieces import Pawn, Rook, Knight, Bishop, King, Queen, BaseChessPiece
# The Chess board is a 8x8 grid of squares
class Board(dict):
    """
    The Chess Board that will be used to play the game.
    It has an setup_board() function that fills a dictionary of squares with the pieces that are in the starting position.
    It has a print_board() function that prints the board to the console.
    It has a find_piece() function that returns the square that a piece is in.
    It has a get_piece() function that returns the piece that is in a square.
    It has a is_square_empty() function that returns True if the square is empty.
    It has a kill_piece() function that kills a piece by setting is_alive boolean to false.
    It has a save_board() function that saves the board to a file.
    """
    def __init__(self):
        # Use a dict comprehension to create a dictionary of squares. The keys are the square names and the values are None.
        # You can use the `range(ord('a'), ord('i'))` to create a range for the alphabetical characters and `range(1, 9)` to create a range for the numbers.
        # Those represent the rows and columns of the chess board
        self.squares = {f'{chr(x)}{y}': None for x in range(ord('a'), ord('i')) for y in range(1, 9)}
        self.setup_board()

        for square, piece in self.squares.items():
            if piece is not None:
                piece.set_initial_position(square)
                piece.define_board(self)

        dict.__init__(self, squares=self.squares)
    
    def setup_board(self):
        """
        Fill the board with the pieces in their starting positions.
        """
        self.squares['a1'] = Rook('BLACK', 1)
        self.squares['b1'] = Knight('BLACK', 1)
        self.squares['c1'] = Bishop('BLACK', 1)
        self.squares['d1'] = Queen('BLACK', 1)
        self.squares['e1'] = King('BLACK', 1)
        self.squares['f1'] = Bishop('BLACK', 2)
        self.squares['g1'] = Knight('BLACK', 2)
        self.squares['h1'] = Rook('BLACK', 2)
        # Use a dict comprehension to add the black pawns on row 2, the keys are the square names and the values are the pieces.
        black_pawns = {
            f"{chr(range(ord('a'), ord('i'))[i - 1])}2": Pawn('BLACK', i) for i in range(1, 9)
        }
        # Update the black pawns to the squares
        self.squares.update(black_pawns)

        # Repeat for the white pawns, they are on rows 7
        white_pawns = {
            f"{chr(range(ord('a'), ord('i'))[i - 1])}7": Pawn('WHITE', i) for i in range(1, 9)
        }
        self.squares.update(white_pawns)


        self.squares['a8'] = Rook('WHITE', 1)
        self.squares['b8'] = Knight('WHITE', 1)
        self.squares['c8'] = Bishop('WHITE', 1)
        self.squares['d8'] = Queen('WHITE', 1)
        self.squares['e8'] = King('WHITE', 1)
        self.squares['f8'] = Bishop('WHITE', 2)
        self.squares['g8'] = Knight('WHITE', 2)
        self.squares['h8'] = Rook('WHITE', 2)

    def print_board(self):
        rows = [
            [self.squares[key] for key in self.squares.keys() if key.endswith(f"{i}")] for i in range(1,9)
        ]
        # Print the rows on different lines in the console
        for row in rows:
            print(row)

    @staticmethod
    def print_saved_board(board):
        rows = [
            [board[key] for key in board.keys() if key.endswith(f"{i}")] for i in range(1,9)
        ]
        # Print the rows on different lines in the console
        for row in rows:
            print(row)
    
    def find_piece(self, symbol: str, identifier: str, color: str):
        """
        Find the piece and the square it's in
        """
        # Search the dictionary values on the symbol, identifier and color properties of the pieces.
        # Return the piece that matches the symbol, identifier and color.
        return [value for value in [value for value in self.squares.values() if value is not None] if value.symbol == symbol and value.identifier == identifier and value.color == color][0]

    def get_piece(self, square):
        """Returns the piece that is on a specific square"""
        return self.squares[square]

    def is_square_empty(self, square):
        """Returns True if the square is empty, False otherwise."""
        return self.get_piece(square) is None

    def kill_piece(self, square):
        """Kills a piece by setting is_alive to False"""
        piece = self.get_piece(square)
        piece.die()
        print(f"{piece} was killed.")

    def save_board(self):
        """Saves the board to a file"""
        saved_file = 'board.txt'
        with open(saved_file, 'a') as file:
            file.write(json.dumps(self.squares))
            file.write('\n')
        print(f"Saved board to txt file: {saved_file}.")
        return saved_file

    @staticmethod
    def get_board_movements():
        """Gets the movements from that board.txt file using a generator"""
        saved_file = 'board.txt'
        with open(saved_file, 'r') as file:
            for line in file:
                yield json.loads(line)