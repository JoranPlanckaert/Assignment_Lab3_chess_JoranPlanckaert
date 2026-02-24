from pieces import Pawn, King, Queen, Bishop, Knight, Rook
from board import Board

board = Board()

print("Initial board: \n")
board.print_board()
board.save_board() # Save the initial board before a movement has been done
print('\n')

# pawn_one_white = board.find_piece('-', 1, 'WHITE')
# pawn_one_black = board.find_piece('-', 1, 'BLACK')
# pawn_one_white.move()
# pawn_one_black.move()
# pawn_one_white.move()
# pawn_one_black.move()
# pawn_one_white.move()

# board_movements = Board.get_board_movements()
# # print(next(board_movements))
# Board.print_saved_board(next(board_movements))
# Board.print_saved_board(next(board_movements))
# Board.print_saved_board(next(board_movements))
# Board.print_saved_board(next(board_movements))
# # print(piece_one)


bishop_one_white = board.find_piece('B', 1, 'BLACK')
bishop_one_white.move('Forward_Right', 2)
bishop_one_white.move('Backward_Left', 2)
# bishop_one_white.move('Right_Forward')
# bishop_one_white.move('Left_Backward')
# bishop_one_white.move('Backward_Left')
board.print_board()