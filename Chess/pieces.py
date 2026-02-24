from abc import ABC, abstractmethod
import functools
import json


class BoardMovements():

    @staticmethod
    def forward(position: str, color: str, squares: int):
        """
        Move the piece forward on the board.
        """
        # Get the column and row of the current position
        column = position[0]
        row = int(position[1])
        # Add the number of squares to the row
        new_row = row + squares  if color == 'BLACK' else row - squares
        # Return the new position
        if (new_row == 0 or new_row == 9):
            print('This piece has reached the boundary of the board.')
            return f"{column}{row}"
        return f"{column}{new_row}"

    @staticmethod
    def backward(position: str, color: str, squares: int):
        """
        Move the piece backward on the board.
        """
        # Get the column and row of the current position
        column = position[0]
        row = int(position[1])
        # Subtract the number of squares to the row
        new_row = row - squares if color == 'BLACK' else row + squares
        # Return the new position
        if (new_row == 0 or new_row == 9):
            print('This piece has reached the boundary of the board.')
            return f"{column}{row}"
        return f"{column}{new_row}"
    
    @staticmethod
    def left(position: str, color: str, squares: int):
        """
        Move the piece left on the board.
        """
        # Get the column and row of the current position
        column = position[0]
        row = int(position[1])
        # Subtract the number of squares to the column
        new_column = chr(ord(column) - squares) if color == 'BLACK' else chr(ord(column) + squares)
        # Return the new position
        if (new_column == '`' or new_column == 'i'):
            print('This piece has reached the boundary of the board.')
            return f"{column}{row}"
        return f"{new_column}{row}"

    @staticmethod
    def right(position: str, color: str, squares: int):
        """
        Move the piece right on the board.
        """
        # Get the column and row of the current position
        column = position[0]
        row = int(position[1])
        # Add the number of squares to the column
        new_column = chr(ord(column) + squares)  if color == 'BLACK' else chr(ord(column) - squares)
        # Return the new position
        if (new_column == '`' or new_column == 'i'):
            print('This piece has reached the boundary of the board.')
            return f"{column}{row}"
        return f"{new_column}{row}"

    @staticmethod
    def diagonally_forward_right(position: str, color: str, squares: int):
        """
        Move the piece diagonally forward right on the board.
        """
        return BoardMovements.right(BoardMovements.forward(position, color, squares), color, squares)

    @staticmethod
    def diagonally_forward_left(position: str, color: str, squares: int):
        """
        Move the piece diagonally forward left on the board.
        """
        return BoardMovements.left(BoardMovements.forward(position, color, squares), color, squares)

    @staticmethod
    def diagonally_backward_left(position: str, color: str, squares: int):
        """
        Move the piece diagonally backward left on the board.
        """
        return BoardMovements.left(BoardMovements.backward(position, color, squares), color, squares)

    @staticmethod
    def diagonally_backward_right(position: str, color: str, squares: int):
        """
        Move the piece diagonally backward right on the board.
        """
        return BoardMovements.right(BoardMovements.backward(position, color, squares), color, squares)



# Base Chess Piece Class (Abstract)
class BaseChessPiece(ABC, dict):

    def __init__(self, color: str, name: str, symbol: str, identifier: int):
        self.color = color
        self.symbol = symbol
        self.name = name # The name to use for the Piece
        self.identifier = identifier # The identifier to use for the Piece in case there are more with the same name
        self.is_alive = True
        self.position = "None"
        dict.__init__(self, color=color, symbol=symbol, identifier=identifier, is_alive=self.is_alive, name=self.name)


    def __str__(self):
        return "{} {} {}".format(self.color, self.name, self.identifier)

    def __repr__(self):
        return "{} {} {}".format(self.color, self.name, self.identifier)


    # def __eq__(self, other):
    #     # Equals when the symbol, identifier and color are the same
    #     return self.symbol == other.symbol and self.identifier == other.identifier and self.color == other.color

    def print_movement(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            print(f"Piece is currently at position {self.position}")
            print(f"Piece is moving ")
            func(self, *args, **kwargs)
            print(f"Piece is now at position {self.position}")
        return wrapper

    def save_board(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            saved_file = self.board.save_board()
        return wrapper

    def reposition(self, movement):
        # Remove the piece from the current position
        self.board.squares[self.position] = None
        # Set the new position
        self.position = movement
        # Add the piece to the new position
        self.board.squares[self.position] = self

    # @print_movement
    @save_board
    @abstractmethod
    def move(self, movement):
        # Check for validity if needed

        # Check if there is already a piece on that 
        other_piece = self.board.get_piece(movement)
        if (other_piece is not None and other_piece.color == self.color):
            print("There is already a piece here, and it's the same colour as yours, so you can't move there.")
        elif (other_piece is not None and other_piece.color != self.color):
            print('There is already a piece here, we will kill it.')
            other_piece.die()
            self.reposition(movement)
        else:
            self.reposition(movement)
            
    def die(self):
        self.board.squares[self.position] = None # Remove it from the board
        self.position = None # Position is cleared
        self.is_alive = False
        print(f"{self} got killed.")

    def set_initial_position(self, position):
        self.position = position

    def define_board(self, board):
        self.board = board
    


class Pawn(BaseChessPiece):

    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Pawn', '-', identifier)

    def move(self):
        movement = BoardMovements.forward(self.position, self.color, 1)
        super().move(movement)

# The rook can move in a straight line, horizontally or vertically, any number of squares.
class Rook(BaseChessPiece):

    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Rook', 'R', identifier)
    
    def move(self, direction, squares):
        if (direction == 'Left'):
            movement = BoardMovements.left(self.position, self.color, squares)
        elif (direction == 'Right'):
            movement = BoardMovements.right(self.position, self.color, squares)
        elif (direction == 'Forward'):
            movement = BoardMovements.forward(self.position, self.color, squares)
        elif (direction == 'Backward'):
            movement = BoardMovements.backward(self.position, self.color, squares)
        super().move(movement)

# The knight moves to any of the closest squares that are not on the same rank, file, or diagonal, thus the move forms an "L"-shape: two squares vertically and one square horizontally, or two squares horizontally and one square vertically. The knight is the only piece that can leap over other pieces.
class Knight(BaseChessPiece):

    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Knight', 'N', identifier)
    
    def move(self, direction):
        if (direction == 'Left_Forward'):
            movement = BoardMovements.forward(BoardMovements.left(self.position, self.color, 2), self.color, 1)
        elif (direction == 'Right_Forward'):
            movement = BoardMovements.forward(BoardMovements.right(self.position, self.color, 2), self.color, 1)
        elif (direction == 'Left_Backward'):
            movement = BoardMovements.backward(BoardMovements.left(self.position, self.color, 2), self.color, 1)
        elif (direction == 'Right_Backward'):
            movement = BoardMovements.backward(BoardMovements.right(self.position, self.color, 2), self.color, 1)
        elif (direction == 'Backward_Right'):
            movement = BoardMovements.backward(BoardMovements.right(self.position, self.color, 1), self.color, 2)
        elif (direction == 'Backward_Left'):
            movement = BoardMovements.backward(BoardMovements.left(self.position, self.color, 1), self.color, 2)
        elif (direction == 'Forward_Right'):
            movement = BoardMovements.forward(BoardMovements.right(self.position, self.color, 1), self.color, 2)
        elif (direction == 'Forward_Left'):
            movement = BoardMovements.forward(BoardMovements.left(self.position, self.color, 1), self.color, 2)
        super().move(movement)

# The bishop can move any number of squares diagonally, but cannot leap over other pieces.
class Bishop(BaseChessPiece):

    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Bishop', 'B', identifier)
    
    def move(self, direction, squares):
        if (direction == 'Backward_Right'):
            movement = BoardMovements.diagonally_backward_right(self.position, self.color, squares)
        elif (direction == 'Backward_Left'):
            movement = BoardMovements.diagonally_backward_left(self.position, self.color, squares)
        elif (direction == 'Forward_Right'):
            movement = BoardMovements.diagonally_forward_right(self.position, self.color, squares)
        elif (direction == 'Forward_Left'):
            movement = BoardMovements.diagonally_forward_left(self.position, self.color, squares)
        super().move(movement)

# The queen combines the power of a rook and bishop and can move any number of squares along a rank, file, or diagonal, but cannot leap over other pieces.
class Queen(BaseChessPiece):

    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'Queen', 'Q', identifier)
    
    def move(self, direction, squares):
        if (direction == 'Left'):
            movement = BoardMovements.left(self.position, self.color, squares)
        elif (direction == 'Right'):
            movement = BoardMovements.right(self.position, self.color, squares)
        elif (direction == 'Forward'):
            movement = BoardMovements.forward(self.position, self.color, squares)
        elif (direction == 'Backward'):
            movement = BoardMovements.backward(self.position, self.color, squares)
        elif (direction == 'Backward_Right'):
            movement = BoardMovements.diagonally_backward_right(self.position, self.color, squares)
        elif (direction == 'Backward_Left'):
            movement = BoardMovements.diagonally_backward_left(self.position, self.color, squares)
        elif (direction == 'Forward_Right'):
            movement = BoardMovements.diagonally_forward_right(self.position, self.color, squares)
        elif (direction == 'Forward_Left'):
            movement = BoardMovements.diagonally_forward_left(self.position, self.color, squares)
        super().move(movement)

# The king moves one square in any direction, so long as that square is not attacked by an enemy piece.
class King(BaseChessPiece):

    def __init__(self, color: str, identifier: int):
        super().__init__(color, 'King', 'K', identifier)
    
    def move(self, direction):
        if (direction == 'Left'):
            movement = BoardMovements.left(self.position, self.color, 1)
        elif (direction == 'Right'):
            movement = BoardMovements.right(self.position, self.color, 1)
        elif (direction == 'Forward'):
            movement = BoardMovements.forward(self.position, self.color, 1)
        elif (direction == 'Backward'):
            movement = BoardMovements.backward(self.position, self.color, 1)
        elif (direction == 'Backward_Right'):
            movement = BoardMovements.diagonally_backward_right(self.position, self.color, 1)
        elif (direction == 'Backward_Left'):
            movement = BoardMovements.diagonally_backward_left(self.position, self.color, 1)
        elif (direction == 'Forward_Right'):
            movement = BoardMovements.diagonally_forward_right(self.position, self.color, 1)
        elif (direction == 'Forward_Left'):
            movement = BoardMovements.diagonally_forward_left(self.position, self.color, 1)

        super().move(movement)