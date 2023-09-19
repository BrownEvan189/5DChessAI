
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


board = [[[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
           [' ', ' ', ' ', ' ', ' ', Piece("king", [0, 0, 4, 5]), ' ', ' '], 
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]]]

print(board[0])
move(board, board[0][0][4][5])
print(board[0])
