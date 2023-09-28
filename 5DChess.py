import copy
import os
from turtle import clear

rank = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

univ0 = 0

def parse_move(m):
    m = m.replace('U', 'T').split('T')

    return {'univ': int(m[1]), 'time': int(m[2][0]), 'x': rank.index(m[2][1]), 'y': int(m[2][2]) - 1, 
            'new_univ': int(m[3]), 'new_time': int(m[4][0]), 'new_x': rank.index(m[4][1]), 'new_y': int(m[4][2]) - 1}

class Piece():
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        if(self.color == 'B'):
            return f'\033[1;31m' + self.name + f'\033[1;37m'
        else:
            return f'\033[1;32m' + self.name + f'\033[1;37m'
        
    def getMovements(self, board, m): # for each piece, add legal movements to 'move' list
        coords = parse_move(m)
        Y_OFFSET = 1

        moves = []

        if self.name == "P" and self.color == "W":

            if coords['y'] == 6 and board[coords['univ']][coords['time']][coords['y']- 2][coords['x']] == ' ': moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']]}{coords['y']- 2 + Y_OFFSET}")
            if coords['y'] > 0 and board[coords['univ']][coords['time']][coords['y']- 1][coords['x']] == ' ': moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']]}{coords['y']- 1 + Y_OFFSET}")
            if coords['univ'] > 0 and len(board[coords['univ'] - 1]) > coords['time'] and len(board[coords['univ'] - 1][coords['time']]) != 0 and board[coords['univ'] - 1][coords['time']][coords['y']][coords['x']] == ' ': moves.append(f"U{coords['univ'] - 1}T{coords['time']}{rank[coords['x']]}{coords['y']+ Y_OFFSET}")
            if coords['y'] > 0 and coords['x'] > 0 and board[coords['univ']][coords['time']][coords['y']- 1][coords['x']- 1] != ' ' and board[coords['univ']][coords['time']][coords['y']- 1][coords['x']- 1].color == 'B': moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']- 1]}{coords['y']- 1 + Y_OFFSET}")
            if coords['y'] > 0 and coords['x'] < len(rank) - 1 and board[coords['univ']][coords['time']][coords['y']- 1][coords['x']+ 1] != ' ' and board[coords['univ']][coords['time']][coords['y']- 1][coords['x']+ 1].color == 'B': moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']+ 1]}{coords['y']- 1 + Y_OFFSET}")

        if self.name == "P" and self.color == "B":

            if coords['y'] == 1 and board[coords['univ']][coords['time']][coords['y']+ 2][coords['x']] == ' ': moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']]}{coords['y']+ 2 + Y_OFFSET}")
            if coords['y'] < 7 and board[coords['univ']][coords['time']][coords['y']+ 1][coords['x']] == ' ': moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']]}{coords['y']+ 1 + Y_OFFSET}")
            if len(board) > coords['univ'] + 1 and len(board[coords['univ'] + 1]) > coords['time'] and board[coords['univ'] + 1][coords['time']][coords['y']][coords['x']] == ' ': moves.append(f"U{coords['univ'] + 1}T{coords['time']}{rank[coords['x']]}{coords['y']+ Y_OFFSET}")
            if coords['y'] < 7 and coords['x'] > 0 and board[coords['univ']][coords['time']][coords['y']+ 1][coords['x']- 1] != ' ' and board[coords['univ']][coords['time']][coords['y']+ 1][coords['x']- 1].color == 'W': moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']- 1]}{coords['y']+ 1 + Y_OFFSET}")
            if coords['y'] < 7 and coords['x'] < len(rank) - 1 and board[coords['univ']][coords['time']][coords['y']+ 1][coords['x']+ 1] != ' ' and board[coords['univ']][coords['time']][coords['y']+ 1][coords['x']+ 1].color == 'W': moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']+ 1]}{coords['y']+ 1 + Y_OFFSET}")
        
        if self.name == "R":
            
            for i in range(coords['x']- 1, -1, -1):
                if board[coords['univ']][coords['time']][coords['y']][i] == ' ':
                    moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[i]}{coords['y']+ Y_OFFSET}")
                elif board[coords['univ']][coords['time']][coords['y']][i].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[i]}{coords['y']+ Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(coords['x']+ 1, 8):
                if board[coords['univ']][coords['time']][coords['y']][i] == ' ':
                    moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[i]}{coords['y']+ Y_OFFSET}")
                elif board[coords['univ']][coords['time']][coords['y']][i].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[i]}{coords['y']+ Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(coords['y']- 1, -1, -1):
                if board[coords['univ']][coords['time']][i][coords['x']] == ' ':
                    moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']]}{i + Y_OFFSET}")
                elif board[coords['univ']][coords['time']][i][coords['x']].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']]}{i + Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(coords['y']+ 1, 8):
                if board[coords['univ']][coords['time']][i][coords['x']] == ' ':
                    moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']]}{i + Y_OFFSET}")
                elif board[coords['univ']][coords['time']][i][coords['x']].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{coords['univ']}T{coords['time'] + 1}{rank[coords['x']]}{i + Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(coords['univ'] - 1, -1, -1):
                if len(board[i]) <= coords['time'] or board[i][coords['time']][0] == ' ':
                    break
                if board[i][coords['time']][coords['y']][coords['x']] == ' ':
                    moves.append(f"U{i}T{coords['time']}{rank[coords['x']]}{coords['y']+ Y_OFFSET}")
                elif board[i][coords['time']][coords['y']][coords['x']].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{i}T{coords['time']}{rank[coords['x']]}{coords['y']+ Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(coords['univ'] + 1, len(board)):
                if len(board[i]) <= coords['time'] or board[i][coords['time']][0] == ' ':
                    break
                if board[i][coords['time']][coords['y']][i] == ' ':
                    moves.append(f"U{i}T{coords['time']}{rank[coords['x']]}{coords['y']+ Y_OFFSET}")
                elif board[i][coords['time']][coords['y']][i].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{i}T{coords['time']}{rank[coords['x']]}{coords['y']+ Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(coords['time'] - 2, -1, -2):
                if board[coords['univ']][i][0] == ' ':
                    break
                if board[coords['univ']][i][coords['y']][coords['x']] == ' ':
                    moves.append(f"U{coords['univ']}T{i}{rank[coords['x']]}{coords['y']+ Y_OFFSET}")
                elif board[coords['univ']][i][coords['y']][coords['x']].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{coords['univ']}T{i}{rank[coords['x']]}{coords['y']+ Y_OFFSET}")
                    break
                else:
                    break
        
        for i in range(len(moves)): moves[i] = m[0:6] + moves[i]
        return moves

def movePiece(board, m):
    global univ0
    coords = parse_move(m)

    board[coords['univ']].append([board[coords['univ']][coords['time']][i][:] for i in range(len(board[coords['univ']][coords['time']]))]) #Copies the previous board into the next time
    
    if coords['time'] == coords['new_time']: #If white is travelling to different universe
        board[coords['new_univ']].append([board[coords['new_univ']][coords['new_time']][i][:] for i in range(len(board[coords['new_univ']][coords['new_time']]))]) #Copies the previous board into the next time

        board[coords['new_univ']][coords['new_time'] + 1][coords['new_y']][coords['new_x']] = board[coords['univ']][coords['time']][coords['y']][coords['x']]
        board[coords['univ']][coords['time'] + 1][coords['y']][coords['x']] = ' '
        return [coords['new_univ'], coords['new_time'] + 1]

    elif coords['time'] + 1 != coords['new_time'] and board[coords['univ']][coords['time']][coords['y']][coords['x']].color == 'W':

        board.append([]) #Increments one universe down 
        for i in range(coords['new_time'] + 1):
            board[len(board) - 1].append(' ')
        board[len(board) - 1].append(copy.deepcopy(board[coords['new_univ']][coords['new_time']]))
        board[len(board) - 1][coords['new_time'] + 1][coords['new_y']][coords['new_x']] = board[coords['univ']][coords['time']][coords['y']][coords['x']]
        board[coords['univ']][coords['time'] + 1][coords['y']][coords['x']] = ' '

        new_coords = [len(board) - 1, coords['new_time'] + 1]
        return new_coords

    elif coords['time'] + 1 != coords['new_time']:
        board.insert(0, []) #Increments one universe up 
        for i in range(coords['new_time'] + 1):
            board[0].append(' ')
        board[0].append(copy.deepcopy(board[coords['new_univ'] + 1][coords['new_time']]))
        board[0][coords['new_time'] + 1][coords['new_y']][coords['new_x']] = board[coords['univ'] + 1][coords['time']][coords['y']][coords['x']]
        board[coords['univ'] + 1][coords['time'] + 1][coords['y']][coords['x']] = ' '

        univ0 += 1
        new_coords = [0, coords['new_time'] + 1]
        return new_coords

    else:
        board[coords['new_univ']][coords['new_time']][coords['new_y']][coords['new_x']] = board[coords['new_univ']][coords['new_time']][coords['y']][coords['x']]
        board[coords['new_univ']][coords['new_time']][coords['y']][coords['x']] = ' '

        if ((board[coords['new_univ']][coords['new_time']][coords['new_y']][coords['new_x']].name == 'P' and board[coords['new_univ']][coords['new_time']][coords['new_y']][coords['new_x']].color == 'W' and coords['new_y'] == 0)
            or (board[coords['new_univ']][coords['new_time']][coords['new_y']][coords['new_x']].name == 'P' and board[coords['new_univ']][coords['new_time']][coords['new_y']][coords['new_x']].color == 'B' and coords['new_y'] == 7)): # change pawn to queen
            board[coords['new_univ']][coords['new_time']][coords['new_y']][coords['new_x']].name = 'Q'

        return [coords['new_univ'], coords['new_time']]


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

view_board(0,0)
while(1):
    move = input("Enter a move: ")
    if move == "map":
        map()
    elif move[0:4] == 'view':
        view_board(int(move[5]), int(move[7]))
    else:
        coords = parse_move(move)
        print(board_array[coords['univ']][coords['time']][coords['y']][coords['x']].getMovements(board_array, move))
        if (board_array[coords['univ']][coords['time']][coords['y']][coords['x']] == ' ' or
             move not in board_array[coords['univ']][coords['time']][coords['y']][coords['x']].getMovements(board_array, move)): # Check if legal move
            print("Illegal move!")
        else:
            new_coords = movePiece(board_array, move)
            view_board(new_coords[0], new_coords[1])
