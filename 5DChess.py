import copy
import os
from turtle import clear

rank = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

univ0 = 0

def parse_move(m):
    m = m.replace('U', 'T').split('T')

    return (int(m[1]), int(m[2][0]), rank.index(m[2][1]), int(m[2][2]) - 1, int(m[3]), int(m[4][0]), rank.index(m[4][1]), int(m[4][2]) - 1)

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
        univ, time, x, y, new_univ, new_time, new_x, new_y = parse_move(m)
        Y_OFFSET = 1
        n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
            
        def queen_check(utboard, x, y, i, n, nw, w, sw, s, se, e, ne):
            qm = []

            if w and x - i > -1:
                if utboard[y][x - i] == ' ':
                    qm.append((x - i, y))
                elif utboard[y][x - i].color == ('W' if self.color == 'B' else 'B'):
                    qm.append((x - i, y))
                    w = False
                else:
                    w = False
            if e and x + i < 8:
                if utboard[y][x + i] == ' ':
                    qm.append((x + i, y))
                elif utboard[y][x + i].color == ('W' if self.color == 'B' else 'B'):
                    qm.append((x + i, y))
                    e = False
                else:
                    e = False
            if n and y - i > -1:
                if utboard[y - i][x] == ' ':
                    qm.append((x, y - i))
                elif utboard[y - i][x].color == ('W' if self.color == 'B' else 'B'):
                    qm.append((x, y - i))
                    n = False
                else:
                    n = False
            if s and y + i < 8:
                if utboard[y + i][x] == ' ':
                    qm.append((x, y + i))
                elif utboard[y + i][x].color == ('W' if self.color == 'B' else 'B'):
                    qm.append((x, y + i))
                    s = False
                else:
                    s = False
            if nw and y - i > -1 and x - i > -1:
                if utboard[y - i][x - i] == ' ':
                    qm.append((x - i, y - i))
                elif utboard[y - i][x - i].color == ('W' if self.color == 'B' else 'B'):
                    qm.append((x - i, y - i))
                    nw = False
                else:
                    nw = False
            if ne and y - i > -1 and x + i < 8:
                if utboard[y - i][x + i] == ' ':
                    qm.append((x + i, y - i))
                elif utboard[y - i][x + i].color == ('W' if self.color == 'B' else 'B'):
                    qm.append((x + i, y - i))
                    ne = False
                else:
                    ne = False
            if sw and y + i < 8 and x - i > -1:
                if utboard[y + i][x - i] == ' ':
                    qm.append((x - i, y + i))
                elif utboard[y + i][x - i].color == ('W' if self.color == 'B' else 'B'):
                    qm.append((x - i, y + i))
                    sw = False
                else:
                    sw = False
            if se and y + i < 8 and x + i < 8:
                if utboard[y + i][x + i] == ' ':
                    qm.append((x + i, y + i))
                elif utboard[y + i][x + i].color == ('W' if self.color == 'B' else 'B'):
                    qm.append((x + i, y + i))
                    se = False
                else:
                    se = False
            return qm

        moves = []

        if self.name == "P" and self.color == "W":

            if y == 6 and board[univ][time][y- 2][x] == ' ': moves.append(f"U{univ}T{time + 1}{rank[x]}{y- 2 + Y_OFFSET}")
            if y > 0 and board[univ][time][y- 1][x] == ' ': moves.append(f"U{univ}T{time + 1}{rank[x]}{y- 1 + Y_OFFSET}")
            if univ > 0 and len(board[univ - 1]) > time and len(board[univ - 1][time]) != 0 and board[univ - 1][time][y][x] == ' ': moves.append(f"U{univ - 1}T{time}{rank[x]}{y+ Y_OFFSET}")
            if y > 0 and x > 0 and board[univ][time][y- 1][x- 1] != ' ' and board[univ][time][y- 1][x- 1].color == 'B': moves.append(f"U{univ}T{time + 1}{rank[x- 1]}{y- 1 + Y_OFFSET}")
            if y > 0 and x < len(rank) - 1 and board[univ][time][y- 1][x+ 1] != ' ' and board[univ][time][y- 1][x+ 1].color == 'B': moves.append(f"U{univ}T{time + 1}{rank[x+ 1]}{y- 1 + Y_OFFSET}")

        elif self.name == "P" and self.color == "B":

            if y == 1 and board[univ][time][y+ 2][x] == ' ': moves.append(f"U{univ}T{time + 1}{rank[x]}{y+ 2 + Y_OFFSET}")
            if y < 7 and board[univ][time][y+ 1][x] == ' ': moves.append(f"U{univ}T{time + 1}{rank[x]}{y+ 1 + Y_OFFSET}")
            if len(board) > univ + 1 and len(board[univ + 1]) > time and board[univ + 1][time][y][x] == ' ': moves.append(f"U{univ + 1}T{time}{rank[x]}{y+ Y_OFFSET}")
            if y < 7 and x > 0 and board[univ][time][y+ 1][x- 1] != ' ' and board[univ][time][y+ 1][x- 1].color == 'W': moves.append(f"U{univ}T{time + 1}{rank[x- 1]}{y+ 1 + Y_OFFSET}")
            if y < 7 and x < len(rank) - 1 and board[univ][time][y+ 1][x+ 1] != ' ' and board[univ][time][y+ 1][x+ 1].color == 'W': moves.append(f"U{univ}T{time + 1}{rank[x+ 1]}{y+ 1 + Y_OFFSET}")
        
        elif self.name == "R":
            
            for i in range(x- 1, -1, -1):
                if board[univ][time][y][i] == ' ':
                    moves.append(f"U{univ}T{time + 1}{rank[i]}{y + Y_OFFSET}")
                elif board[univ][time][y][i].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{univ}T{time + 1}{rank[i]}{y + Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(x+ 1, 8):
                if board[univ][time][y][i] == ' ':
                    moves.append(f"U{univ}T{time + 1}{rank[i]}{y + Y_OFFSET}")
                elif board[univ][time][y][i].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{univ}T{time + 1}{rank[i]}{y + Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(y- 1, -1, -1):
                if board[univ][time][i][x] == ' ':
                    moves.append(f"U{univ}T{time + 1}{rank[x]}{i + Y_OFFSET}")
                elif board[univ][time][i][x].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{univ}T{time + 1}{rank[x]}{i + Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(y+ 1, 8):
                if board[univ][time][i][x] == ' ':
                    moves.append(f"U{univ}T{time + 1}{rank[x]}{i + Y_OFFSET}")
                elif board[univ][time][i][x].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{univ}T{time + 1}{rank[x]}{i + Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(univ - 1, -1, -1):
                if len(board[i]) <= time or board[i][time][0] == ' ':
                    break
                if board[i][time][y][x] == ' ':
                    moves.append(f"U{i}T{time}{rank[x]}{y + Y_OFFSET}")
                elif board[i][time][y][x].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{i}T{time}{rank[x]}{y + Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(univ + 1, len(board)):
                if len(board[i]) <= time or board[i][time][0] == ' ':
                    break
                if board[i][time][y][i] == ' ':
                    moves.append(f"U{i}T{time}{rank[x]}{y + Y_OFFSET}")
                elif board[i][time][y][i].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{i}T{time}{rank[x]}{y + Y_OFFSET}")
                    break
                else:
                    break
            
            for i in range(time - 2, -1, -2):
                if board[univ][i][0] == ' ':
                    break
                if board[univ][i][y][x] == ' ':
                    moves.append(f"U{univ}T{i}{rank[x]}{y + Y_OFFSET}")
                elif board[univ][i][y][x].color == ('W' if self.color == 'B' else 'B'):
                    moves.append(f"U{univ}T{i}{rank[x]}{y + Y_OFFSET}")
                    break
                else:
                    break
        
        elif self.name == 'N':
            
            for i in range(-2, 3): # x-positions in the first half, universes in the second half
                if i != 0 and x + i > -1 and x + i < 8:
                    delta_y = 3 - abs(i)
                    if (y + delta_y < 8 and (board[univ][time][y + delta_y][x + i] == ' ' or
                            board[univ][time][y + delta_y][x + i].color == ('W' if self.color == 'B' else 'B'))):
                        moves.append(f"U{univ}T{time + 1}{rank[x + i]}{y + delta_y + Y_OFFSET}")
                    if (y - delta_y > -1 and (board[univ][time][y - delta_y][x + i] == ' ' or
                            board[univ][time][y - delta_y][x + i].color == ('W' if self.color == 'B' else 'B'))):
                        moves.append(f"U{univ}T{time + 1}{rank[x + i]}{y - delta_y + Y_OFFSET}")

                if univ + i > -1 and univ + i < len(board):
                    for j in range(-2 * (3 - abs(i)), 2 * (3 - abs(i)) + 1, 2):
                        if time + j > -1 and len(board[univ + i]) > time + j and board[univ + i][time + j][0] != ' ':
                            if (abs(i) == 2 and abs(j) == 2) or (abs(i) == 1 and abs(j) == 4):
                                if ((board[univ + i][time + j][y][x] == ' ' or
                                        board[univ + i][time + j][y][x].color == ('W' if self.color == 'B' else 'B'))):
                                    moves.append(f"U{univ + i}T{time + j}{rank[x]}{y + Y_OFFSET}")

                            elif (abs(i) == 2 and j == 0) or (i == 0 and abs(j) == 4):
                                for k in range(-1, 2):
                                    delta_y = 1 - abs(k)
                                    if (x + k > -1 and x + k < 8 and y + delta_y < 8 and
                                            (board[univ + i][time + j][y + delta_y][x + k] == ' ' or
                                            board[univ + i][time + j][y + delta_y][x + k].color == ('W' if self.color == 'B' else 'B'))):
                                        moves.append(f"U{univ + i}T{time + j}{rank[x + k]}{y + delta_y + Y_OFFSET}")
                                    if (x + k > -1 and x + k < 8 and y - delta_y > -1 and
                                            (board[univ + i][time + j][y - delta_y][x + k] == ' ' or
                                            board[univ + i][time + j][y - delta_y][x + k].color == ('W' if self.color == 'B' else 'B'))):
                                        moves.append(f"U{univ + i}T{time + j}{rank[x + k]}{y - delta_y + Y_OFFSET}")
                            
                            elif (abs(i) == 1 and j == 0) or (i == 0 and abs(j) == 2):
                                for k in range(-2, 3, 2):
                                    delta_y = 2 - abs(k)
                                    if (x + k > -1 and x + k < 8 and y + delta_y < 8 and
                                            (board[univ + i][time + j][y + delta_y][x + k] == ' ' or
                                            board[univ + i][time + j][y + delta_y][x + k].color == ('W' if self.color == 'B' else 'B'))):
                                        moves.append(f"U{univ + i}T{time + j}{rank[x + k]}{y + delta_y + Y_OFFSET}")
                                    if (x + k > -1 and x + k < 8 and y - delta_y > -1 and
                                            (board[univ + i][time + j][y - delta_y][x + k] == ' ' or
                                            board[univ + i][time + j][y - delta_y][x + k].color == ('W' if self.color == 'B' else 'B'))):
                                        moves.append(f"U{univ + i}T{time + j}{rank[x + k]}{y - delta_y + Y_OFFSET}")
        
        elif self.name == 'B':
            #Regular moves for a bishop
            
            #input('1')
            bishop_array = [[8, -1, 1, -1], [8, 8, 1, 1], [-1, 8, -1, 1], [-1, -1, -1, -1]]
            for k in bishop_array:
                i = x + k[2]
                j = y + k[3]
                while (i != k[0] and j != k[1]):
                    if board[univ][time][j][i] != ' ':
                        if board[univ][time][j][i].color != self.color:
                            moves.append(f"U{univ}T{time + 1}{rank[i]}{j + 1}")
                            #input(f'x={i}, y={j}')
                        break
                    else:
                        moves.append(f"U{univ}T{time + 1}{rank[i]}{j + 1}")
                        #input(f'x={i}, y={j}')
                    i += k[2]
                    j += k[3]
            
            #input('2')
            #Bishop moving across universes bishop_array = [x-bound, y-bound, x-inc, y-inc, univ-direction, univ-bound] -2 means null
            bishop_array = [[8, -2, 1, 0, 1, len(board)], [8, -2, 1, 0, -1, -1], #Positive x dir
                            [-1, -2, -1, 0, 1, len(board)], [-1, -2, -1, 0, -1, -1], #Negative x dir
                            [-2, 8, 0, 1, 1, len(board)], [-2, 8, 0, 1, -1, -1], #Positive y dir
                            [-2, -1, 0, -1, 1, len(board)], [-2, -1, 0, -1, -1, -1]] #Negative y dir
            for k in bishop_array:
                i = x + k[2]
                j = y + k[3]
                u = univ + k[4]
                while (i != k[0] and j != k[1] and u != k[5]):
                    if len(board[u]) >= time + 1:
                        if board[u][time][j][i] != ' ':
                            if board[univ][time][j][i].color != self.color:
                                moves.append(f"U{u}T{time}{rank[i]}{j + 1}")
                                #input(f"U:{u}, U:{time}")
                                #input(f'x={i}, y={j}')
                            break
                        else:
                            moves.append(f"U{u}T{time}{rank[i]}{j + 1}")
                            #input(f'x={i}, y={j}')
                            #input(f"U:{u}, U:{time}")
                        i += k[2]
                        j += k[3]
                        u += k[4]
                    else:
                        break
            
            #input('3')
            #Bishop travelling back in time - bishop_array = [x-bound, y-bound, x-inc, y-inc, -1, 0]
            bishop_array = [[8, -2, 1, 0], [-1, -2, -1, 0], [-2, 8, 0, 1], [-2, -1, 0, -1]] 
            for k in bishop_array:
                i = x + k[2]
                j = y + k[3]
                t = time - 2
                while (i != k[0] and j != k[1] and t >= 0):
                    if board[univ][t] != ' ':
                        if board[univ][t][j][i] != ' ':
                            if board[univ][t][j][i].color != self.color:
                                moves.append(f"U{univ}T{t}{rank[i]}{j + 1}")
                            break
                        else:
                            moves.append(f"U{univ}T{t}{rank[i]}{j + 1}")
                        i += k[2]
                        j += k[3]
                        t -= 2

            #Bishop travelling across time and universes - bishop_array = [u-inc, t-inc]
            #input('4')
            bishop_array = [[1, 2], [-1, 2], [1, -2], [-1, -2]]
            for k in bishop_array:
                u = univ + k[0]
                t = time + k[1]
                #if u >= 0 and t >= 0:
                #input(k)
                while (u >= 0 and u <= len(board) - 1 and t >= 0 and t <= len(board[u]) - 1):
                    if len(board[u]) >= t + 1:
                        if board[u][t] != ' ':
                            if board[u][t][y][x] != ' ':
                                if board[univ][time][y][x].color != self.color:
                                    moves.append(f"U{u}T{t}{rank[x]}{y + 1}")
                                    #input(f'U={u}, T={t}')
                                break
                            else:
                                moves.append(f"U{u}T{t}{rank[x]}{y + 1}")
                                #input(f'U={u}, T={t}')
                            u += k[0]
                            t += k[1]
                        else:
                            break

        elif self.name == 'Q':
            n, ne, e, se, s, sw, w, nw = [True for i in range(8)]

            for i in range(1, max(x + 1, y + 1)):
                if x - i > -1 and w:
                    if board[univ][time][y][x - i] == ' ':
                        moves.append(f"U{univ}T{time + 1}{rank[x - i]}{y + Y_OFFSET}")
                    elif board[univ][time][y][x - i].color == ('W' if self.color == 'B' else 'B'):
                        moves.append(f"U{univ}T{time + 1}{rank[x - i]}{y + Y_OFFSET}")
                        w = False
                    else:
                        w = False

                if y - i > -1 and n:
                    if board[univ][time][y - i][x] == ' ':
                        moves.append(f"U{univ}T{time + 1}{rank[x]}{y - i + Y_OFFSET}")
                    elif board[univ][time][y - i][x].color == ('W' if self.color == 'B' else 'B'):
                        moves.append(f"U{univ}T{time + 1}{rank[x]}{y - i + Y_OFFSET}")
                        n = False
                    else:
                        n = False

                if x - i > -1 and y - i > -1 and nw:
                    if board[univ][time][y - i][x - i] == ' ':
                        moves.append(f"U{univ}T{time + 1}{rank[x - i]}{y - i + Y_OFFSET}")
                    elif board[univ][time][y - i][x - i].color == ('W' if self.color == 'B' else 'B'):
                        moves.append(f"U{univ}T{time + 1}{rank[x - i]}{y - i + Y_OFFSET}")
                        nw = False
                    else:
                        nw = False
                if x - i > -1 and y + i < 8 and sw:
                    if board[univ][time][y + i][x - i] == ' ':
                        moves.append(f"U{univ}T{time + 1}{rank[x - i]}{y + i + Y_OFFSET}")
                    elif board[univ][time][y + i][x - i].color == ('W' if self.color == 'B' else 'B'):
                        moves.append(f"U{univ}T{time + 1}{rank[x - i]}{y + i + Y_OFFSET}")
                        sw = False
                    else:
                        sw = False

            for i in range(1, max(8 - x, 8 - y)):
                if x + i < 8 and e:
                    if board[univ][time][y][x + i] == ' ':
                        moves.append(f"U{univ}T{time + 1}{rank[x + i]}{y + Y_OFFSET}")
                    elif board[univ][time][y][x + i].color == ('W' if self.color == 'B' else 'B'):
                        moves.append(f"U{univ}T{time + 1}{rank[x + i]}{y + Y_OFFSET}")
                        e = False
                    else:
                        e = False

                if y + i < 8 and s:
                    if board[univ][time][y + i][x] == ' ':
                        moves.append(f"U{univ}T{time + 1}{rank[x]}{y + i + Y_OFFSET}")
                    elif board[univ][time][y + i][x].color == ('W' if self.color == 'B' else 'B'):
                        moves.append(f"U{univ}T{time + 1}{rank[x]}{y + i + Y_OFFSET}")
                        s = False
                    else:
                        s = False

                if x + i < 8 and y - i > -1 and ne:
                    if board[univ][time][y - i][x + i] == ' ':
                        moves.append(f"U{univ}T{time + 1}{rank[x + i]}{y - i + Y_OFFSET}")
                    elif board[univ][time][y - i][x + i].color == ('W' if self.color == 'B' else 'B'):
                        moves.append(f"U{univ}T{time + 1}{rank[x + i]}{y - i + Y_OFFSET}")
                        ne = False
                    else:
                        ne = False
                if x + i < 8 and y + i < 8 and se:
                    if board[univ][time][y + i][x + i] == ' ':
                        moves.append(f"U{univ}T{time + 1}{rank[x + i]}{y + i + Y_OFFSET}")
                    elif board[univ][time][y + i][x + i].color == ('W' if self.color == 'B' else 'B'):
                        moves.append(f"U{univ}T{time + 1}{rank[x + i]}{y + i + Y_OFFSET}")
                        se = False
                    else:
                        se = False

            n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
            for i in range(1, univ + 1):
                if len(board[univ - i]) > time and board[univ - i][time][0] != ' ':
                    qc = queen_check(board[univ - i][time], x, y, i, n, ne, e, se, s, sw, w, nw)
                    for qcx, qcy in qc:
                        moves.append(f"U{univ - i}T{time}{rank[qcx]}{qcy + Y_OFFSET}")
                        
            n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
            for i in range(1, len(board) - univ):
                if len(board[univ + i]) > time and board[univ + i][time][0] != ' ':
                    qc = queen_check(board[univ + i][time], x, y, i, n, ne, e, se, s, sw, w, nw)
                    for qcx, qcy in qc:
                        moves.append(f"U{univ + i}T{time}{rank[qcx]}{qcy + Y_OFFSET}")
                        
            n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
            for i in range(2, time + 1, 2):
                if board[univ][time - int(i / 2)][0] != ' ':
                    qc = queen_check(board[univ][time - i], x, y, i, n, ne, e, se, s, sw, w, nw)
                    print(qc)
                    for qcx, qcy in qc:
                        moves.append(f"U{univ}T{time - i}{rank[qcx]}{qcy + Y_OFFSET}")
                        
            n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
            for i in range(1, max(univ + 1, int(time / 2) + 1)):
                if univ - i > -1 and time - (i * 2) > -1 and len(board[univ - i]) > time - (i * 2) and board[univ - i][time - (i * 2)][0] != ' ':
                    qc = queen_check(board[univ - i][time - (i * 2)], x, y, i, n, ne, e, se, s, sw, w, nw)
                    for qcx, qcy in qc:
                        moves.append(f"U{univ - i}T{time - (i * 2)}{rank[qcx]}{qcy + Y_OFFSET}")
                        
            n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
            for i in range(1, max(len(board) - univ, int(time / 2) + 1)):
                if univ + i < len(board) and time - (i * 2) > -1 and len(board[univ + i]) > time - (i * 2) and board[univ + i][time - (i * 2)][0] != ' ':
                    qc = queen_check(board[univ + i][time - (i * 2)], x, y, i, n, ne, e, se, s, sw, w, nw)
                    for qcx, qcy in qc:
                        moves.append(f"U{univ + i}T{time - (i * 2)}{rank[qcx]}{qcy + Y_OFFSET}")
                        
            n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
            for i in range(1, len(board)):
                if univ - i > -1:
                    if len(board[univ - i]) > time + (i * 2) and board[univ - i][time + (i * 2)][0] != ' ':
                        qc = queen_check(board[univ - i][time + (i * 2)], x, y, i, n, ne, e, se, s, sw, w, nw)
                        for qcx, qcy in qc:
                            moves.append(f"U{univ - i}T{time + (i * 2)}{rank[qcx]}{qcy + Y_OFFSET}")
                else:
                    break
                
            n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
            for i in range(1, len(board)):
                if univ + i < len(board):
                    if len(board[univ + i]) > time + (i * 2) and board[univ + i][time + (i * 2)][0] != ' ':
                        qc = queen_check(board[univ + i][time + (i * 2)], x, y, i, n, ne, e, se, s, sw, w, nw)
                        for qcx, qcy in qc:
                            moves.append(f"U{univ + i}T{time + (i * 2)}{rank[qcx]}{qcy + Y_OFFSET}")
                else:
                    break
        
        if self.name == "K":

            for i in range(-1, 2):
                for j in range(-2, 3, 2):
                    if univ + i > -1 and time + j > -1 and univ + i < len(board) and len(board[univ + i]) > time + j and board[univ + i][time + j][0] != ' ':
                        kc = queen_check(board[univ + i][time + j], x, y, 1, True, True, True, True, True, True, True, True)
                        for kcx, kcy in kc:
                            moves.append(f"U{univ + i}T{time + j + (1 if j == 0 else 0)}{rank[kcx]}{kcy + Y_OFFSET}")
        
        for i in range(len(moves)): moves[i] = m[0:6] + moves[i]
        return moves

def movePiece(board, m):
    global univ0
    univ, time, x, y, new_univ, new_time, new_x, new_y = parse_move(m)

    board[univ].append([board[univ][time][i][:] for i in range(len(board[univ][time]))]) #Copies the previous board into the next time
    
    if new_univ != univ and len(board[new_univ]) == new_time + 1: #Traveling to new universe at latest point in its timeline
        board[new_univ].append([board[new_univ][new_time][i][:] for i in range(len(board[new_univ][new_time]))])

        board[new_univ][new_time + 1][new_y][new_x] = board[univ][time][y][x]
        board[univ][time + 1][y][x] = ' '
        return [new_univ, new_time + 1]

    elif ((new_univ != univ or time + 1 != new_time)
           and board[univ][time][y][x].color == 'W'): # White traveling to a board not at the latest point in time

        board.append([]) #Increments one universe down 
        for i in range(new_time + 1):
            board[len(board) - 1].append(' ')
        board[len(board) - 1].append(copy.deepcopy(board[new_univ][new_time]))
        board[len(board) - 1][new_time + 1][new_y][new_x] = board[univ][time][y][x]
        board[univ][time + 1][y][x] = ' '

        new_coords = [len(board) - 1, new_time + 1]
        return new_coords

    elif new_univ != univ or time + 1 != new_time: # Black traveling to a board not at the latest point in time
        board.insert(0, []) #Increments one universe up 
        for i in range(new_time + 1):
            board[0].append(' ')
        board[0].append(copy.deepcopy(board[new_univ + 1][new_time]))
        board[0][new_time + 1][new_y][new_x] = board[univ + 1][time][y][x]
        board[univ + 1][time + 1][y][x] = ' '

        univ0 += 1
        new_coords = [0, new_time + 1]
        return new_coords

    else: # Normal move
        board[new_univ][new_time][new_y][new_x] = board[new_univ][new_time][y][x]
        board[new_univ][new_time][y][x] = ' '

        if ((board[new_univ][new_time][new_y][new_x].name == 'P' and board[new_univ][new_time][new_y][new_x].color == 'W' and new_y == 0)
            or (board[new_univ][new_time][new_y][new_x].name == 'P' and board[new_univ][new_time][new_y][new_x].color == 'B' and new_y == 7)): # change pawn to queen
            board[new_univ][new_time][new_y][new_x].name = 'Q'

        return [new_univ, new_time]


current_board = [
    [Piece('R', 'B'),Piece('N', 'B'),Piece('B', 'B'),Piece('Q', 'B'),Piece('K', 'B'),Piece('B', 'B'),Piece('N', 'B'),Piece('R', 'B')],
    [Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B'),Piece('P', 'B')],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W'),Piece('P', 'W')],
    [Piece('R', 'W'),Piece('N', 'W'),Piece('B', 'W'),Piece('Q', 'W'),Piece('K', 'W'),Piece('B', 'W'),Piece('N', 'W'),Piece('R', 'W')],
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
        univ, time, x, y, new_univ, new_time, new_x, new_y = parse_move(move)
        print(board_array[univ][time][y][x].getMovements(board_array, move))
        if (board_array[univ][time][y][x] == ' ' or
             move not in board_array[univ][time][y][x].getMovements(board_array, move)): # Check if legal move
            print("Illegal move!")
        else:
            new_coords = movePiece(board_array, move)
            view_board(new_coords[0], new_coords[1])
