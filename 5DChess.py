
class Piece():
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord

    def getMovements(self):
        if self.name == "king":
            return [0, 0, 1, 0]
            
        
def movePiece(board, piece):
    move = piece.getMovements()
    board[piece.coord[0] + move[0]][piece.coord[1] + move[1]][piece.coord[2] + move[2]][piece.coord[3] + move[3]] = piece
    board[piece.coord[0]][piece.coord[1]][piece.coord[2]][piece.coord[3]] = ' '
    piece.coord = [piece.coord[0] + move[0], piece.coord[1] + move[1], piece.coord[2] + move[2], piece.coord[3] + move[3]]
        
def move(board, piece):
    board[piece.coord[0]].append(board[piece.coord[0]][piece.coord[1]])
    movePiece(board, board[piece.coord[0]][piece.coord[1] + 1][piece.coord[2]][piece.coord[3]])


current_board = [
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',Piece("king,[0,0,4,5],' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
]





def view_board(univ, time):
    current_board = board_array[univ][time]
    print('+---+---+---+---+---+---+---+---+')
    print(f'| {current_board[0][0]} | {current_board[0][1]} | {current_board[0][2]} | {current_board[0][3]} | {current_board[0][4]} | {current_board[0][5]} | {current_board[0][6]} | {current_board[0][7]} |')
    print('+---+---+---+---+---+---+---+---+')
    print(f'| {current_board[1][0]} | {current_board[1][1]} | {current_board[1][2]} | {current_board[1][3]} | {current_board[1][4]} | {current_board[1][5]} | {current_board[1][6]} | {current_board[1][7]} |')
    print('+---+---+---+---+---+---+---+---+')
    print(f'| {current_board[2][0]} | {current_board[2][1]} | {current_board[2][2]} | {current_board[2][3]} | {current_board[2][4]} | {current_board[2][5]} | {current_board[2][6]} | {current_board[2][7]} |')
    print('+---+---+---+---+---+---+---+---+')
    print(f'| {current_board[3][0]} | {current_board[3][1]} | {current_board[3][2]} | {current_board[3][3]} | {current_board[3][4]} | {current_board[3][5]} | {current_board[3][6]} | {current_board[3][7]} |')
    print('+---+---+---+---+---+---+---+---+')
    print(f'| {current_board[4][0]} | {current_board[4][1]} | {current_board[4][2]} | {current_board[4][3]} | {current_board[4][4]} | {current_board[4][5]} | {current_board[4][6]} | {current_board[4][7]} |')
    print('+---+---+---+---+---+---+---+---+')
    print(f'| {current_board[5][0]} | {current_board[5][1]} | {current_board[5][2]} | {current_board[5][3]} | {current_board[5][4]} | {current_board[5][5]} | {current_board[5][6]} | {current_board[5][7]} |')
    print('+---+---+---+---+---+---+---+---+')
    print(f'| {current_board[6][0]} | {current_board[6][1]} | {current_board[6][2]} | {current_board[6][3]} | {current_board[6][4]} | {current_board[6][5]} | {current_board[6][6]} | {current_board[6][7]} |')
    print('+---+---+---+---+---+---+---+---+')
    print(f'| {current_board[7][0]} | {current_board[7][1]} | {current_board[7][2]} | {current_board[7][3]} | {current_board[7][4]} | {current_board[7][5]} | {current_board[7][6]} | {current_board[7][7]} |')
    print('+---+---+---+---+---+---+---+---+')
board_array = [
    []
]

board_array.append(current_board)

print(board_array[0])
move(board_array, board_array[0][0][4][5])
view_board(0,0)
view_board(0,1)
