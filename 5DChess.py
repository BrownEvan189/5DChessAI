import copy

rank = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
univ0 = 0

class Piece():
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        if(self.color == 'B'):
            return f'\033[1;31m' + self.name + f'\033[1;37m'
        else:
            return f'\033[1;32m' + self.name + f'\033[1;37m'

    def getMovements(self):
        if self.name == "K":
            return [0, 0, 1, 0]
            
        
def movePiece(board, m):
    m = m.replace('U', 'T').split('T')
    univ = int(m[1])
    time = int(m[2][0])
    x = rank.index(m[2][1])
    y = int(m[2][2]) - 1
    new_univ = int(m[3])
    new_time = int(m[4][0])
    new_x = rank.index(m[4][1])
    new_y = int(m[4][2]) - 1
    
    board[univ].append([board[univ][time][i][:] for i in range(len(board[univ][time]))])

    if time + 1 != new_time and board[univ][time][y][x].color == 'W':
        board.append([[[]]])
        for i in range(new_time):
            board[len(board) - 1].append([[]])
        board[len(board) - 1].append(board[new_univ][new_time])
        
        board[len(board) - 1][new_time + 1][new_y][new_x] = copy.copy(board[univ][time][y][x])
        board[len(board) - 1][new_time + 1][y][x] = ' '

    elif time + 1 != new_time:
        board.insert(0, [[[]]])
        for i in range(new_time):
            board[0].append([[]])
        board[0].append(board[new_univ][new_time])
        
        board[0][new_time + 1][new_y][new_x] = board[univ][time][y][x]
        board[0][new_time + 1][y][x] = ' '

        univ0 += 1

    else:
        board[new_univ][new_time][new_y][new_x] = board[new_univ][new_time][y][x]
        board[new_univ][new_time][y][x] = ' '


current_board = [
    [Piece('R', 'B'),Piece('K', 'B'),Piece('B', 'B'),Piece('Q', 'B'),Piece('K', 'B'),Piece('B', 'B'),Piece('K', 'B'),Piece('R', 'B')],
    [Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B')],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W')],
    [Piece('R', 'W'),Piece('K', 'W'),Piece('B', 'W'),Piece('Q', 'W'),Piece('K', 'W'),Piece('B', 'W'),Piece('K', 'W'),Piece('R', 'W')],
]


board_array = [
    []
]

board_array[0].append(current_board)


def view_board(univ, time):
    current_board = board_array[univ][time]
    print('board ' + str(univ) + ' ' + str(time))
    print('   +---+---+---+---+---+---+---+---+')
    print(f' 1 | {current_board[0][0]} | {current_board[0][1]} | {current_board[0][2]} | {current_board[0][3]} | {current_board[0][4]} | {current_board[0][5]} | {current_board[0][6]} | {current_board[0][7]} |')
    print('   +---+---+---+---+---+---+---+---+')
    print(f' 2 | {current_board[1][0]} | {current_board[1][1]} | {current_board[1][2]} | {current_board[1][3]} | {current_board[1][4]} | {current_board[1][5]} | {current_board[1][6]} | {current_board[1][7]} |')
    print('   +---+---+---+---+---+---+---+---+')
    print(f' 3 | {current_board[2][0]} | {current_board[2][1]} | {current_board[2][2]} | {current_board[2][3]} | {current_board[2][4]} | {current_board[2][5]} | {current_board[2][6]} | {current_board[2][7]} |')
    print('   +---+---+---+---+---+---+---+---+')
    print(f' 4 | {current_board[3][0]} | {current_board[3][1]} | {current_board[3][2]} | {current_board[3][3]} | {current_board[3][4]} | {current_board[3][5]} | {current_board[3][6]} | {current_board[3][7]} |')
    print('   +---+---+---+---+---+---+---+---+')
    print(f' 5 | {current_board[4][0]} | {current_board[4][1]} | {current_board[4][2]} | {current_board[4][3]} | {current_board[4][4]} | {current_board[4][5]} | {current_board[4][6]} | {current_board[4][7]} |')
    print('   +---+---+---+---+---+---+---+---+')
    print(f' 6 | {current_board[5][0]} | {current_board[5][1]} | {current_board[5][2]} | {current_board[5][3]} | {current_board[5][4]} | {current_board[5][5]} | {current_board[5][6]} | {current_board[5][7]} |')
    print('   +---+---+---+---+---+---+---+---+')
    print(f' 7 | {current_board[6][0]} | {current_board[6][1]} | {current_board[6][2]} | {current_board[6][3]} | {current_board[6][4]} | {current_board[6][5]} | {current_board[6][6]} | {current_board[6][7]} |')
    print('   +---+---+---+---+---+---+---+---+')
    print(f' 8 | {current_board[7][0]} | {current_board[7][1]} | {current_board[7][2]} | {current_board[7][3]} | {current_board[7][4]} | {current_board[7][5]} | {current_board[7][6]} | {current_board[7][7]} |')
    print('   +---+---+---+---+---+---+---+---+')
    print('     a | b | c | d | e | f | g | h')

def map():
    for j in range(len(board_array)):
        for i in range(len(board_array[j])):
            print(f'[{j},{i}]',end='')
        print('\n')

command = input("Enter a command: ")
if command == "play":
    view_board(0,0)
    while(1):
        move = input("Enter a move: ")
        if move == "map":
            map()
        elif move[0:4] == 'view':
            view_board(int(move[5]), int(move[7]))
        else:
            movePiece(board_array, move)

            m = move.replace('U', 'T').split('T')
            univ = int(m[1])
            time = int(m[2][0])
            x = rank.index(m[2][1])
            y = int(m[2][2]) - 1

            view_board(int(m[3]), int(m[4][0]))


        



