import copy
import os
from turtle import clear

rank = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

univ0 = 0

def parse_move(m):
    m = m.replace('U', 'T').split('T')
    univ = int(m[1])
    time = int(m[2][0])
    x = rank.index(m[2][1])
    y = int(m[2][2]) - 1
    new_univ = int(m[3])
    new_time = int(m[4][0])
    new_x = rank.index(m[4][1])
    new_y = int(m[4][2]) - 1

    return {'univ': univ, 'time': time, 'x': x, 'y': y, 'new_univ': new_univ, 'new_time': new_time, 'new_x': new_x, 'new_y': new_y}

class Piece():
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        if(self.color == 'B'):
            return f'\033[1;31m' + self.name + f'\033[1;37m'
        else:
            return f'\033[1;32m' + self.name + f'\033[1;37m'
        
    def getMovements(self, board, m):
        coords = parse_move(m)
        univ = coords['univ']
        time = coords['time']
        x = coords['x']
        y = coords['y']

        moves = []

        if self.name == "P" and self.color == "W":
            moves = [f"U{univ}T{time + 1}{x}{y - 2}", f"U{univ}T{time + 1}{x}{y - 1}", f"U{univ + 1}T{time}{x}{y}", f"U{univ}T{time}{rank[x - 1]}{y - 1}", f"U{univ}T{time + 1}{rank[x + 1]}{y - 1}"]

            if y != 7:
                moves.remove(f"U{univ}T{time + 1}{x}{y - 2}")
            if board[univ + 1][time][y][x] != ' ':
                moves.remove(f"U{univ + 1}T{time}{x}{y}")
            if board[univ][time + 1][y - 1][x] != ' ':
                moves.remove(f"U{univ}T{time + 1}{x}{y - 1}")
            if board[univ][time + 1][y - 1][x - 1].color != 'B':
                moves.remove(f"U{univ}T{time}{rank[x - 1]}{y - 1}")
            if board[univ][time + 1][y - 1][x + 1].color != 'B':
                moves.remove(f"U{univ}T{time}{rank[x + 1]}{y - 1}")

        if self.name == "P" and self.color == "B":
            moves = [f"U{univ}T{time + 1}{x}{y + 2}", f"U{univ}T{time + 1}{x}{y + 1}", f"U{univ + 1}T{time}{x}{y}", f"U{univ}T{time}{rank[x - 1]}{y + 1}", f"U{univ}T{time + 1}{rank[x + 1]}{y + 1}"]

            if y != 7:
                pawn_moves.remove(f"U{univ}T{time + 1}{x}{y + 2}")
            if board[univ + 1][time][y][x] != ' ':
                pawn_moves.remove(f"U{univ + 1}T{time}{x}{y}")
            if board[univ][time + 1][y - 1][x] != ' ':
                pawn_moves.remove(f"U{univ}T{time + 1}{x}{y + 1}")
            if board[univ][time + 1][y - 1][x - 1].color != 'W':
                pawn_moves.remove(f"U{univ}T{time}{rank[x - 1]}{y + 1}")
            if board[univ][time + 1][y - 1][x + 1].color != 'W':
                pawn_moves.remove(f"U{univ}T{time}{rank[x + 1]}{y + 1}")
        
        if self.name == "R":
            
            for i in range(x, 1, -1):
                if board[univ][time][y][i] == ' ':
                    moves.append[f"U{univ}T{time + 1}{rank[i]}{y}"]
                elif board[univ][time][y][i] == ('W' if self.color == 'B' else 'B'):
                    moves.append[f"U{univ}T{time + 1}{rank[i]}{y}"]
                    break
                else:
                    break
            
            for i in range(x, 8):
                if board[univ][time][y][i] == ' ':
                    moves.append[f"U{univ}T{time + 1}{rank[i]}{y}"]
                elif board[univ][time][y][i] == ('W' if self.color == 'B' else 'B'):
                    moves.append[f"U{univ}T{time + 1}{rank[i]}{y}"]
                    break
                else:
                    break
            
            for i in range(y, 1, -1):
                if board[univ][time][y][i] == ' ':
                    moves.append[f"U{univ}T{time + 1}{rank[x]}{i}"]
                elif board[univ][time][y][i] == ('W' if self.color == 'B' else 'B'):
                    moves.append[f"U{univ}T{time + 1}{rank[x]}{i}"]
                    break
                else:
                    break
            
            for i in range(y, 8):
                if board[univ][time][y][i] == ' ':
                    moves.append[f"U{univ}T{time + 1}{rank[x]}{i}"]
                elif board[univ][time][y][i] == ('W' if self.color == 'B' else 'B'):
                    moves.append[f"U{univ}T{time + 1}{rank[x]}{i}"]
                    break
                else:
                    break
            
            for i in range(0, univ, -1):
                if board[univ][time][y][i] == ' ':
                    moves.append[f"U{i}T{time}{rank[x]}{y}"]
                elif board[univ][time][y][i] == ('W' if self.color == 'B' else 'B'):
                    moves.append[f"U{i}T{time}{rank[x]}{y}"]
                    break
                else:
                    break
            
            for i in range(univ, len(board)):
                if board[univ][time][y][i] == ' ':
                    moves.append[f"U{i}T{time}{rank[x]}{y}"]
                elif board[univ][time][y][i] == ('W' if self.color == 'B' else 'B'):
                    moves.append[f"U{i}T{time}{rank[x]}{y}"]
                    break
                else:
                    break
            
            for i in range(0, time, -2):
                if board[univ][time][y][i] == ' ':
                    moves.append[f"U{univ}T{i}{rank[x]}{y}"]
                elif board[univ][time][y][i] == ('W' if self.color == 'B' else 'B'):
                    moves.append[f"U{univ}T{i}{rank[x]}{y}"]
                    break
                else:
                    break
        
        return moves

def movePiece(board, m):
    global univ0
    coords = parse_move(m)
    univ = coords['univ']
    time = coords['time']
    x = coords['x']
    y = coords['y']
    new_univ = coords['new_univ']
    new_time = coords['new_time']
    new_x = coords['new_x']
    new_y = coords['new_y']

    board[univ].append([board[univ][time][i][:] for i in range(len(board[univ][time]))]) #Copies the previous board into the next time
    
    if time == new_time: #If white is travelling back in time
        board[new_univ].append([board[new_univ][new_time][i][:] for i in range(len(board[new_univ][new_time]))]) #Copies the previous board into the next time

        board[new_univ][new_time + 1][new_y][new_x] = board[univ][time][y][x]
        board[univ][time + 1][y][x] = ' '
        return [new_univ, new_time + 1]

    elif time + 1 != new_time and board[univ][time][y][x].color == 'W':

        board.append([]) #Increments one universe down 
        for i in range(new_time + 1):
            board[univ + 1].append(' ')
        board[univ + 1].append(copy.deepcopy(board[new_univ][new_time]))
        board[univ + 1][new_time + 1][new_y][new_x] = board[univ][time][y][x]
        board[univ][time + 1][y][x] = ' '

        new_coords = [new_univ + 1, new_time + 1]
        return new_coords

    elif time + 1 != new_time:
        board.insert(0, []) #Increments one universe down 
        for i in range(new_time + 1):
            board[0].append(' ')
        board[0].append(copy.deepcopy(board[new_univ + 1][new_time]))
        board[0][new_time + 1][new_y][new_x] = board[univ + 1][time][y][x]
        board[univ + 1][time + 1][y][x] = ' '

        univ0 += 1
        new_coords = [0, new_time + 1]
        return new_coords

    else:
        board[new_univ][new_time][new_y][new_x] = board[new_univ][new_time][y][x]
        board[new_univ][new_time][y][x] = ' '

        if board[new_univ][new_time][new_y][new_x].name == 'P':
            board[new_univ][new_time][new_y][new_x].name = 'Q'

        return [new_univ, new_time]


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
    if  univ0 > 0:
        print('U |')
    else:
        print('U|')
    for j in range(len(board_array)):
        if j - univ0 < 0:
            print(f'{j - univ0}|',end='')
        else:
             print(f'{j - univ0} |',end='')           
        for i in range(len(board_array[j])):
            if board_array[j][i] == ' ':
                print('     ',end='')
            else:
                print(f'[{j},{i}]',end='')
        print()

os.system('clear')
#command = input("Enter a command: ")
#if command == "play":
view_board(0,0)
while(1):
    move = input("Enter a move: ")
    coords = parse_move(move)
    if move not in board_array[coords['univ']][coords['time']][coords['y']][coords['x']].getMovements(board_array, move):
        print("Illegal move!")
    elif move == "map":
        map()
    elif move[0:4] == 'view':
        view_board(int(move[5]), int(move[7]))
    else:
        new_coords = movePiece(board_array, move)
        view_board(new_coords[0], new_coords[1])
