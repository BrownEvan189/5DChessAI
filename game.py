import os
from copy import deepcopy

class Game():

    def __init__(self):
        self.rank = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        self.positions = {}
        self.attack_lines = {}
        self.attacks = {}
        self.kings = []
        self.check = []

        self.univ0 = 0
        self.last_univ0 = 0
        self.present = 0

        self.pres_count = 0

        self.board_array = [[[
                    [self.createPiece('R', 'B'),self.createPiece('N', 'B'),self.createPiece('B', 'B'),self.createPiece('Q', 'B'),self.createPiece('K', 'B'),self.createPiece('B', 'B'),self.createPiece('N', 'B'),self.createPiece('R', 'B')],
                    [self.createPiece('P', 'B'),self.createPiece('P', 'B'),self.createPiece('P', 'B'),self.createPiece('P', 'B'),self.createPiece('P', 'B'),self.createPiece('P', 'B'),self.createPiece('P', 'B'),self.createPiece('P', 'B')],
                    [' ',' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' ',' '],
                    [self.createPiece('P', 'W'),self.createPiece('P', 'W'),self.createPiece('P', 'W'),self.createPiece('P', 'W'),self.createPiece('P', 'W'),self.createPiece('P', 'W'),self.createPiece('P', 'W'),self.createPiece('P', 'W')],
                    [self.createPiece('R', 'W'),self.createPiece('N', 'W'),self.createPiece('B', 'W'),self.createPiece('Q', 'W'),self.createPiece('K', 'W'),self.createPiece('B', 'W'),self.createPiece('N', 'W'),self.createPiece('R', 'W')],
                ]]]

        for i in range(len(self.board_array[0][0])):
            for j in range(len(self.board_array[0][0][i])):
                piece = self.board_array[0][0][i][j]
                if piece != ' ':
                    if piece.name == 'K':
                        self.kings.append((0, 0, i, j))
                    if (0, 0) not in self.positions:
                        self.positions[(0, 0)] = {}
                    if piece.name not in self.positions[(0, 0)]:
                        self.positions[(0, 0)][piece.name] = [(j, i)]
                    else:
                        self.positions[(0, 0)][piece.name].append((j, i))
                    pgm = piece.getMovements(self.board_array, f"U0T0{self.rank[j]}{i + 1}U0T1a1", att=True)
                    for k in range(len(pgm)):
                        pgm[k] = pgm[k][6:]
                        if pgm[k] not in self.attack_lines:
                            self.attack_lines[pgm[k]] = []
                        self.attack_lines[pgm[k]].append((0, 0, i, j))
                    self.attacks[(0, 0, i, j)] = pgm

        self.name_array = ['P', 'R', 'N', 'B', 'K', 'Q']

    def parse_move(self, m):
        m = m.replace('U', 'T').split('T')
        t = ""
        i = 0
        while(m[2][i] not in self.rank):
            t += m[2][i]
            i += 1
        
        t2 = ""
        j = 0
        while(m[4][j] not in self.rank):
            t2 += m[4][j]
            j += 1

        return (int(m[1]), int(t), self.rank.index(m[2][i]), int(m[2][i + 1]) - 1, int(m[3]), int(t2), self.rank.index(m[4][j]), int(m[4][j + 1]) - 1)
    

    def createPiece(self, name, color, status = ""):
        return self.Piece(self, name, color, status)

    def new_board_att_lines(self, board, univ, time):
        Y_OFFSET = 1

        for new_univ in range(len(board)):
            if univ != new_univ:
                new_time = len(board[new_univ]) - 1
                if abs(new_univ - univ) == 2 * abs(new_time - time):
                    if "Q" in self.positions[(new_univ - self.univ0, new_time)]:
                        for pos in self.positions[(new_univ - self.univ0, new_time)]["Q"]:
                            for i in range(new_univ - univ, univ - new_univ, univ - new_univ):
                                for j in range(new_univ - univ, univ - new_univ, univ - new_univ):
                                    if pos[0] + i > -1 and pos[0] + i < 8 and pos[1] + j > -1 and pos[1] + j < 8:
                                        if f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}" not in self.attack_lines:
                                            self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"] = []
                                        self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"].append((new_univ - self.univ0, new_time, pos[1], pos[0]))
                                        self.attacks[(new_univ - self.univ0, new_time, pos[1], pos[0])].append(f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}")

                    if "B" in self.positions[(new_univ - self.univ0, new_time)]:
                        for pos in self.positions[(new_univ - self.univ0, new_time)]["B"]:
                            if f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}" not in self.attack_lines:
                                self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}"] = []
                            self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}"].append((new_univ - self.univ0, new_time, pos[1], pos[0]))
                            self.attacks[(new_univ - self.univ0, new_time, pos[1], pos[0])].append(f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}")
                    
                if new_time - time == 0:
                    if "Q" in self.positions[(new_univ - self.univ0, new_time)]:
                        for pos in self.positions[(new_univ - self.univ0, new_time)]["Q"]:
                            for i in range(new_univ - univ, univ - new_univ, univ - new_univ):
                                for j in range(new_univ - univ, univ - new_univ, univ - new_univ):
                                    if pos[0] + i > -1 and pos[0] + i < 8 and pos[1] + j > -1 and pos[1] + j < 8:
                                        if f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}" not in self.attack_lines:
                                            self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"] = []
                                        self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"].append((new_univ - self.univ0, new_time, pos[1], pos[0]))
                                        self.attacks[(new_univ - self.univ0, new_time, pos[1], pos[0])].append(f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}")

                    if "B" in self.positions[(new_univ - self.univ0, new_time)]:
                        for pos in self.positions[(new_univ - self.univ0, new_time)]["B"]:
                            delta = abs(new_univ - univ)
                            for i in range(-delta, delta, delta):
                                delta_y =  delta - abs(i)
                                for j in range(-delta_y, delta_y, max(1, 2 * delta_y)):
                                    if pos[0] + i > -1 and pos[0] + i < 8 and pos[1] + j > -1 and pos[1] + j < 8:
                                        if f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}" not in self.attack_lines:
                                            self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"] = []
                                        self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"].append((new_univ - self.univ0, new_time, pos[1], pos[0]))
                                        self.attacks[(new_univ - self.univ0, new_time, pos[1], pos[0])].append(f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}")
                    
                    if "R" in self.positions[(new_univ - self.univ0, new_time)]:
                        for pos in self.positions[(new_univ - self.univ0, new_time)]["R"]:
                            if f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}" not in self.attack_lines:
                                self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}"] = []
                            self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}"].append((new_univ - self.univ0, new_time, pos[1], pos[0]))
                            self.attacks[(new_univ - self.univ0, new_time, pos[1], pos[0])].append(f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}")
            
                if abs(new_univ - univ) == 1 and abs(new_time - time) in (0, 2) and "K" in self.positions[(new_univ - self.univ0, new_time)]:
                    for pos in self.positions[(new_univ - self.univ0, new_time)]["K"]:
                        for i in range(-1, 1):
                            for j in range(-1, 1):
                                if pos[0] + i > -1 and pos[0] + i < 8 and pos[1] + j > -1 and pos[1] + j < 8:
                                    if f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}" not in self.attack_lines:
                                        self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"] = []
                                    self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"].append((new_univ - self.univ0, new_time, pos[1], pos[0]))
                                    self.attacks[(new_univ - self.univ0, new_time, pos[1], pos[0])].append(f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}")
                
                if (abs(new_univ - univ), abs(new_time - time)) in [(1, 4), (2, 2)] and "N" in self.positions[(new_univ - self.univ0, new_time)]:
                    for pos in self.positions[(new_univ - self.univ0, new_time)]["N"]:
                        if f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}" not in self.attack_lines:
                            self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}"] = []
                        self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}"].append((new_univ - self.univ0, new_time, pos[1], pos[0]))
                        self.attacks[(new_univ - self.univ0, new_time, pos[1], pos[0])].append(f"U{univ - self.univ0}T{time}{self.rank[pos[0]]}{pos[1] + Y_OFFSET}")

                elif abs(new_univ - univ) == 1 and abs(new_time - time) == 0 and "N" in self.positions[(new_univ - self.univ0, new_time)]:
                    for pos in self.positions[(new_univ - self.univ0, new_time)]["N"]:
                        for i in range(-1, 1):
                            delta_y =  1 - abs(i)
                            for j in range(-delta_y, delta_y, max(1, 2 * delta_y)):
                                if pos[0] + i > -1 and pos[0] + i < 8 and pos[1] + j > -1 and pos[1] + j < 8:
                                    if f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}" not in self.attack_lines:
                                        self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"] = []
                                    self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"].append((new_univ - self.univ0, new_time, pos[1], pos[0]))
                                    self.attacks[(new_univ - self.univ0, new_time, pos[1], pos[0])].append(f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}")

                elif abs(new_univ - univ) == 2 and abs(new_time - time) == 0 and "N" in self.positions[(new_univ - self.univ0, new_time)]:
                    for pos in self.positions[(new_univ - self.univ0, new_time)]["N"]:
                        for i in range(-2, 2, 2):
                            delta_y =  2 - abs(i)
                            for j in range(-delta_y, delta_y, max(1, 2 * delta_y)):
                                if pos[0] + i > -1 and pos[0] + i < 8 and pos[1] + j > -1 and pos[1] + j < 8:
                                    if f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}" not in self.attack_lines:
                                        self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"] = []
                                    self.attack_lines[f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}"].append((new_univ - self.univ0, new_time, pos[1], pos[0]))
                                    self.attacks[(new_univ - self.univ0, new_time, pos[1], pos[0])].append(f"U{univ - self.univ0}T{time}{self.rank[pos[0] + i]}{pos[1] + j + Y_OFFSET}")

    class Piece():
        def __init__(self, game, name, color, status = ""):
            self.game = game
            self.name = name
            self.color = color
            self.status = status

        def __str__(self):
            if(self.color == 'B'):
                return f'\033[1;31m' + self.name + f'\033[1;37m'
            else:
                return f'\033[1;32m' + self.name + f'\033[1;37m'

        def getMovements(self, board, m, att=False): # for each piece, add legal movements to 'move' list
            univ, time, x, y, new_univ, new_time, new_x, new_y = self.game.parse_move(m)
            Y_OFFSET = 1
            n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
                
            def queen_check(x, y, i, n, nw, w, sw, s, se, e, ne, utboard):
                qm = []

                if w and x - i > -1:
                    if utboard[y][x - i] == ' ':
                        qm.append((x - i, y))
                    elif utboard[y][x - i].color == ('W' if self.color == 'B' else 'B') or att:
                        qm.append((x - i, y))
                        w = False
                    else:
                        w = False
                if e and x + i < 8:
                    if utboard[y][x + i] == ' ':
                        qm.append((x + i, y))
                    elif utboard[y][x + i].color == ('W' if self.color == 'B' else 'B') or att:
                        qm.append((x + i, y))
                        e = False
                    else:
                        e = False
                if n and y - i > -1:
                    if utboard[y - i][x] == ' ':
                        qm.append((x, y - i))
                    elif utboard[y - i][x].color == ('W' if self.color == 'B' else 'B') or att:
                        qm.append((x, y - i))
                        n = False
                    else:
                        n = False
                if s and y + i < 8:
                    if utboard[y + i][x] == ' ':
                        qm.append((x, y + i))
                    elif utboard[y + i][x].color == ('W' if self.color == 'B' else 'B') or att:
                        qm.append((x, y + i))
                        s = False
                    else:
                        s = False
                if nw and y - i > -1 and x - i > -1:
                    if utboard[y - i][x - i] == ' ':
                        qm.append((x - i, y - i))
                    elif utboard[y - i][x - i].color == ('W' if self.color == 'B' else 'B') or att:
                        qm.append((x - i, y - i))
                        nw = False
                    else:
                        nw = False
                if ne and y - i > -1 and x + i < 8:
                    if utboard[y - i][x + i] == ' ':
                        qm.append((x + i, y - i))
                    elif utboard[y - i][x + i].color == ('W' if self.color == 'B' else 'B') or att:
                        qm.append((x + i, y - i))
                        ne = False
                    else:
                        ne = False
                if sw and y + i < 8 and x - i > -1:
                    if utboard[y + i][x - i] == ' ':
                        qm.append((x - i, y + i))
                    elif utboard[y + i][x - i].color == ('W' if self.color == 'B' else 'B') or att:
                        qm.append((x - i, y + i))
                        sw = False
                    else:
                        sw = False
                if se and y + i < 8 and x + i < 8:
                    if utboard[y + i][x + i] == ' ':
                        qm.append((x + i, y + i))
                    elif utboard[y + i][x + i].color == ('W' if self.color == 'B' else 'B') or att:
                        qm.append((x + i, y + i))
                        se = False
                    else:
                        se = False
                return qm

            moves = []

            if self.name == "P" and self.color == "W":

                if y == 6 and board[univ][time][y - 2][x] == ' ' and not att:
                    moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{y - 2 + Y_OFFSET}")
                if y > 0 and board[univ][time][y - 1][x] == ' ' and not att:
                    moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{y - 1 + Y_OFFSET}")
                if univ > 0 and len(board[univ - 1]) > time and board[univ - 1][time] != ' ' and board[univ - 1][time][y][x] == ' ' and not att:
                    moves.append(f"U{univ - 1}T{time}{self.game.rank[x]}{y + Y_OFFSET}")
                if y > 0 and x > 0 and (att or (board[univ][time][y - 1][x - 1] != ' ' and board[univ][time][y - 1][x - 1].color == 'B')):
                    moves.append(f"U{univ}T{time + 1}{self.game.rank[x - 1]}{y - 1 + Y_OFFSET}")
                if y > 0 and x < 7 and (att or (board[univ][time][y - 1][x + 1] != ' ' and board[univ][time][y - 1][x + 1].color == 'B')):
                    moves.append(f"U{univ}T{time + 1}{self.game.rank[x + 1]}{y - 1 + Y_OFFSET}")

            elif self.name == "P" and self.color == "B":

                if y == 1 and board[univ][time][y + 2][x] == ' ' and not att:
                    moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{y + 2 + Y_OFFSET}")
                if y < 7 and board[univ][time][y + 1][x] == ' ' and not att:
                    moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{y + 1 + Y_OFFSET}")
                if len(board) > univ + 1 and len(board[univ + 1]) > time and board[univ + 1][time] != ' ' and board[univ + 1][time][y][x] == ' ' and not att:
                    moves.append(f"U{univ + 1}T{time}{self.game.rank[x]}{y + Y_OFFSET}")
                if y < 7 and x > 0 and (att or (board[univ][time][y + 1][x - 1] != ' ' and board[univ][time][y + 1][x - 1].color == 'W')):
                    moves.append(f"U{univ}T{time + 1}{self.game.rank[x - 1]}{y + 1 + Y_OFFSET}")
                if y < 7 and x < 7 and (att or (board[univ][time][y + 1][x + 1] != ' ' and board[univ][time][y + 1][x + 1].color == 'W')):
                    moves.append(f"U{univ}T{time + 1}{self.game.rank[x + 1]}{y + 1 + Y_OFFSET}")
            
            elif self.name == "R":
                
                for i in range(x- 1, -1, -1):
                    if board[univ][time][y][i] == ' ':
                        moves.append(f"U{univ}T{time + 1}{self.game.rank[i]}{y + Y_OFFSET}")
                    elif board[univ][time][y][i].color == ('W' if self.color == 'B' else 'B') or att:
                        moves.append(f"U{univ}T{time + 1}{self.game.rank[i]}{y + Y_OFFSET}")
                        break
                    else:
                        break
                
                for i in range(x+ 1, 8):
                    if board[univ][time][y][i] == ' ':
                        moves.append(f"U{univ}T{time + 1}{self.game.rank[i]}{y + Y_OFFSET}")
                    elif board[univ][time][y][i].color == ('W' if self.color == 'B' else 'B') or att:
                        moves.append(f"U{univ}T{time + 1}{self.game.rank[i]}{y + Y_OFFSET}")
                        break
                    else:
                        break
                
                for i in range(y- 1, -1, -1):
                    if board[univ][time][i][x] == ' ':
                        moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{i + Y_OFFSET}")
                    elif board[univ][time][i][x].color == ('W' if self.color == 'B' else 'B') or att:
                        moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{i + Y_OFFSET}")
                        break
                    else:
                        break
                
                for i in range(y+ 1, 8):
                    if board[univ][time][i][x] == ' ':
                        moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{i + Y_OFFSET}")
                    elif board[univ][time][i][x].color == ('W' if self.color == 'B' else 'B') or att:
                        moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{i + Y_OFFSET}")
                        break
                    else:
                        break
                
                for i in range(univ - 1, -1, -1):
                    if len(board[i]) <= time or board[i][time][0] == ' ':
                        break
                    elif board[i][time][y][x] == ' ':
                        moves.append(f"U{i}T{time}{self.game.rank[x]}{y + Y_OFFSET}")
                    elif board[i][time][y][x].color == ('W' if self.color == 'B' else 'B') or att:
                        moves.append(f"U{i}T{time}{self.game.rank[x]}{y + Y_OFFSET}")
                        break
                    else:
                        break
                
                for i in range(univ + 1, len(board)):
                    if len(board[i]) <= time or board[i][time][0] == ' ':
                        break
                    elif board[i][time][y][i] == ' ':
                        moves.append(f"U{i}T{time}{self.game.rank[x]}{y + Y_OFFSET}")
                    elif board[i][time][y][i].color == ('W' if self.color == 'B' else 'B') or att:
                        moves.append(f"U{i}T{time}{self.game.rank[x]}{y + Y_OFFSET}")
                        break
                    else:
                        break
                
                for i in range(time - 2, -1, -2):
                    if board[univ][i][0] == ' ':
                        break
                    elif board[univ][i][y][x] == ' ':
                        moves.append(f"U{univ}T{i}{self.game.rank[x]}{y + Y_OFFSET}")
                    elif board[univ][i][y][x].color == ('W' if self.color == 'B' else 'B') or att:
                        moves.append(f"U{univ}T{i}{self.game.rank[x]}{y + Y_OFFSET}")
                        break
                    else:
                        break
            
            elif self.name == 'N':
                
                for i in range(-2, 3): # x-self.positions in the first half, universes in the second half
                    if i != 0 and x + i > -1 and x + i < 8:
                        delta_y = 3 - abs(i)
                        if (y + delta_y < 8 and (board[univ][time][y + delta_y][x + i] == ' ' or
                                board[univ][time][y + delta_y][x + i].color == ('W' if self.color == 'B' else 'B') or att)):
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y + delta_y + Y_OFFSET}")
                        if (y - delta_y > -1 and (board[univ][time][y - delta_y][x + i] == ' ' or
                                board[univ][time][y - delta_y][x + i].color == ('W' if self.color == 'B' else 'B') or att)):
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y - delta_y + Y_OFFSET}")

                    if univ + i > -1 and univ + i < len(board):
                        for j in range(-2 * (3 - abs(i)), 2 * (3 - abs(i)) + 1, 2):
                            if (time + j > -1 and len(board[univ + i]) > time + j and board[univ + i][time + j][0] != ' '):
                                if (abs(i) == 2 and abs(j) == 2) or (abs(i) == 1 and abs(j) == 4):
                                    if (att or (board[univ + i][time + j][y][x] == ' ' or
                                            board[univ + i][time + j][y][x].color == ('W' if self.color == 'B' else 'B'))):
                                        moves.append(f"U{univ + i}T{time + j}{self.game.rank[x]}{y + Y_OFFSET}")

                                elif (abs(i) == 2 and j == 0) or (i == 0 and abs(j) == 4):
                                    for k in range(-1, 2):
                                        delta_y = 1 - abs(k)
                                        if (x + k > -1 and x + k < 8 and y + delta_y < 8 and
                                                (att or board[univ + i][time + j][y + delta_y][x + k] == ' ' or
                                                board[univ + i][time + j][y + delta_y][x + k].color == ('W' if self.color == 'B' else 'B'))):
                                            moves.append(f"U{univ + i}T{time + j}{self.game.rank[x + k]}{y + delta_y + Y_OFFSET}")
                                        if (x + k > -1 and x + k < 8 and y - delta_y > -1 and
                                                (att or board[univ + i][time + j][y - delta_y][x + k] == ' ' or
                                                board[univ + i][time + j][y - delta_y][x + k].color == ('W' if self.color == 'B' else 'B'))):
                                            moves.append(f"U{univ + i}T{time + j}{self.game.rank[x + k]}{y - delta_y + Y_OFFSET}")
                                
                                elif (abs(i) == 1 and j == 0) or (i == 0 and abs(j) == 2):
                                    for k in range(-2, 3, 2):
                                        delta_y = 2 - abs(k)
                                        if (x + k > -1 and x + k < 8 and y + delta_y < 8 and
                                                (att or board[univ + i][time + j][y + delta_y][x + k] == ' ' or
                                                board[univ + i][time + j][y + delta_y][x + k].color == ('W' if self.color == 'B' else 'B'))):
                                            moves.append(f"U{univ + i}T{time + j}{self.game.rank[x + k]}{y + delta_y + Y_OFFSET}")
                                        if (x + k > -1 and x + k < 8 and y - delta_y > -1 and
                                                (att or board[univ + i][time + j][y - delta_y][x + k] == ' ' or
                                                board[univ + i][time + j][y - delta_y][x + k].color == ('W' if self.color == 'B' else 'B'))):
                                            moves.append(f"U{univ + i}T{time + j}{self.game.rank[x + k]}{y - delta_y + Y_OFFSET}")
            
            elif self.name == 'B':
                ne, se, sw, nw = [True for i in range(4)]

                for i in range(1, max(x + 1, y + 1)):
                    if x - i > -1 and y - i > -1 and nw:
                        if board[univ][time][y - i][x - i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y - i + Y_OFFSET}")
                        elif board[univ][time][y - i][x - i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y - i + Y_OFFSET}")
                            nw = False
                        else:
                            nw = False
                    if x - i > -1 and y + i < 8 and sw:
                        if board[univ][time][y + i][x - i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y + i + Y_OFFSET}")
                        elif board[univ][time][y + i][x - i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y + i + Y_OFFSET}")
                            sw = False
                        else:
                            sw = False

                for i in range(1, max(8 - x, 8 - y)):
                    if x + i < 8 and y - i > -1 and ne:
                        if board[univ][time][y - i][x + i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y - i + Y_OFFSET}")
                        elif board[univ][time][y - i][x + i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y - i + Y_OFFSET}")
                            ne = False
                        else:
                            ne = False
                    if x + i < 8 and y + i < 8 and se:
                        if board[univ][time][y + i][x + i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y + i + Y_OFFSET}")
                        elif board[univ][time][y + i][x + i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y + i + Y_OFFSET}")
                            se = False
                        else:
                            se = False

                n, e, s, w = [True for i in range(4)]
                for i in range(1, univ + 1):
                    if len(board[univ - i]) > time and board[univ - i][time][0] != ' ':
                        qc = queen_check(x, y, i, n, False, e, False, s, False, w, False, utboard=board[univ - i][time])
                        for qcx, qcy in qc:
                            moves.append(f"U{univ - i}T{time}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                            
                n, e, s, w = [True for i in range(4)]
                for i in range(1, len(board) - univ):
                    if len(board[univ + i]) > time and board[univ + i][time][0] != ' ':
                        qc = queen_check(x, y, i, n, False, e, False, s, False, w, False, utboard=board[univ + i][time])
                        for qcx, qcy in qc:
                            moves.append(f"U{univ + i}T{time}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                            
                n, e, s, w = [True for i in range(4)]
                for i in range(2, time + 1, 2):
                    if board[univ][time - i][0] != ' ':
                        qc = queen_check(x, y, int(i / 2), n, False, e, False, s, False, w, False, utboard=board[univ][time - i])
                        for qcx, qcy in qc:
                            moves.append(f"U{univ}T{time - i}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                            
                for i in range(1, max(univ + 1, int(time / 2) + 1)):
                    if univ - i > -1 and time - (i * 2) > -1 and len(board[univ - i]) > time - (i * 2) and board[univ - i][time - (i * 2)][0] != ' ':
                        if board[univ - i][time - (i * 2)][y][x] == ' ':
                            moves.append(f"U{univ - i}T{time - (i * 2)}{self.game.rank[x]}{y + Y_OFFSET}")
                        elif board[univ - i][time - (i * 2)][y][x].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ - i}T{time - (i * 2)}{self.game.rank[x]}{y + Y_OFFSET}")
                            break
                        else:
                            break
                            
                for i in range(1, max(len(board) - univ, int(time / 2) + 1)):
                    if univ + i < len(board) and time - (i * 2) > -1 and len(board[univ + i]) > time - (i * 2) and board[univ + i][time - (i * 2)][0] != ' ':
                        if board[univ + i][time - (i * 2)][y][x] == ' ':
                            moves.append(f"U{univ + i}T{time - (i * 2)}{self.game.rank[x]}{y + Y_OFFSET}")
                        elif board[univ + i][time - (i * 2)][y][x].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ + i}T{time - (i * 2)}{self.game.rank[x]}{y + Y_OFFSET}")
                            break
                        else:
                            break
                            
                for i in range(1, len(board)):
                    if univ - i > -1 and len(board[univ - i]) > time + (i * 2) and board[univ - i][time + (i * 2)][0] != ' ':
                        if board[univ - i][time + (i * 2)][y][x] == ' ':
                            moves.append(f"U{univ - i}T{time + (i * 2)}{self.game.rank[x]}{y + Y_OFFSET}")
                        elif board[univ - i][time + (i * 2)][y][x].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ - i}T{time + (i * 2)}{self.game.rank[x]}{y + Y_OFFSET}")
                            break
                        else:
                            break
                    
                for i in range(1, len(board)):
                    if univ + i < len(board) and len(board[univ + i]) > time + (i * 2) and board[univ + i][time + (i * 2)][0] != ' ':
                        if board[univ + i][time + (i * 2)][y][x] == ' ':
                            moves.append(f"U{univ + i}T{time + (i * 2)}{self.game.rank[x]}{y + Y_OFFSET}")
                        elif board[univ + i][time + (i * 2)][y][x].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ + i}T{time + (i * 2)}{self.game.rank[x]}{y + Y_OFFSET}")
                            break
                        else:
                            break

            elif self.name == 'Q':
                n, ne, e, se, s, sw, w, nw = [True for i in range(8)]

                for i in range(1, max(x + 1, y + 1)):
                    if x - i > -1 and w:
                        if board[univ][time][y][x - i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y + Y_OFFSET}")
                        elif board[univ][time][y][x - i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y + Y_OFFSET}")
                            w = False
                        else:
                            w = False

                    if y - i > -1 and n:
                        if board[univ][time][y - i][x] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{y - i + Y_OFFSET}")
                        elif board[univ][time][y - i][x].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{y - i + Y_OFFSET}")
                            n = False
                        else:
                            n = False

                    if x - i > -1 and y - i > -1 and nw:
                        if board[univ][time][y - i][x - i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y - i + Y_OFFSET}")
                        elif board[univ][time][y - i][x - i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y - i + Y_OFFSET}")
                            nw = False
                        else:
                            nw = False
                    if x - i > -1 and y + i < 8 and sw:
                        if board[univ][time][y + i][x - i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y + i + Y_OFFSET}")
                        elif board[univ][time][y + i][x - i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x - i]}{y + i + Y_OFFSET}")
                            sw = False
                        else:
                            sw = False

                for i in range(1, max(8 - x, 8 - y)):
                    if x + i < 8 and e:
                        if board[univ][time][y][x + i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y + Y_OFFSET}")
                        elif board[univ][time][y][x + i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y + Y_OFFSET}")
                            e = False
                        else:
                            e = False

                    if y + i < 8 and s:
                        if board[univ][time][y + i][x] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{y + i + Y_OFFSET}")
                        elif board[univ][time][y + i][x].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x]}{y + i + Y_OFFSET}")
                            s = False
                        else:
                            s = False

                    if x + i < 8 and y - i > -1 and ne:
                        if board[univ][time][y - i][x + i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y - i + Y_OFFSET}")
                        elif board[univ][time][y - i][x + i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y - i + Y_OFFSET}")
                            ne = False
                        else:
                            ne = False
                    if x + i < 8 and y + i < 8 and se:
                        if board[univ][time][y + i][x + i] == ' ':
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y + i + Y_OFFSET}")
                        elif board[univ][time][y + i][x + i].color == ('W' if self.color == 'B' else 'B') or att:
                            moves.append(f"U{univ}T{time + 1}{self.game.rank[x + i]}{y + i + Y_OFFSET}")
                            se = False
                        else:
                            se = False

                n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
                for i in range(1, univ + 1):
                    if len(board[univ - i]) > time and board[univ - i][time][0] != ' ':
                        qc = queen_check(x, y, i, n, ne, e, se, s, sw, w, nw, utboard=board[univ - i][time])
                        for qcx, qcy in qc:
                            moves.append(f"U{univ - i}T{time}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                            
                n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
                for i in range(1, len(board) - univ):
                    if len(board[univ + i]) > time and board[univ + i][time][0] != ' ':
                        qc = queen_check(x, y, i, n, ne, e, se, s, sw, w, nw, utboard=board[univ + i][time])
                        for qcx, qcy in qc:
                            moves.append(f"U{univ + i}T{time}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                            
                n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
                for i in range(2, time + 1, 2):
                    if board[univ][time - i][0] != ' ':
                        qc = queen_check(x, y, int(i / 2), n, ne, e, se, s, sw, w, nw, utboard=board[univ][time - i])
                        for qcx, qcy in qc:
                            moves.append(f"U{univ}T{time - i}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                            
                n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
                for i in range(1, max(univ + 1, int(time / 2) + 1)):
                    if univ - i > -1 and time - (i * 2) > -1 and len(board[univ - i]) > time - (i * 2) and board[univ - i][time - (i * 2)][0] != ' ':
                        qc = queen_check(x, y, i, n, ne, e, se, s, sw, w, nw, utboard=board[univ - i][time - (i * 2)])
                        for qcx, qcy in qc:
                            moves.append(f"U{univ - i}T{time - (i * 2)}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                            
                n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
                for i in range(1, max(len(board) - univ, int(time / 2) + 1)):
                    if univ + i < len(board) and time - (i * 2) > -1 and len(board[univ + i]) > time - (i * 2) and board[univ + i][time - (i * 2)][0] != ' ':
                        qc = queen_check(x, y, i, n, ne, e, se, s, sw, w, nw, utboard=board[univ + i][time - (i * 2)])
                        for qcx, qcy in qc:
                            moves.append(f"U{univ + i}T{time - (i * 2)}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                            
                n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
                for i in range(1, len(board)):
                    if univ - i > -1:
                        if len(board[univ - i]) > time + (i * 2) and board[univ - i][time + (i * 2)][0] != ' ':
                            qc = queen_check(x, y, i, n, ne, e, se, s, sw, w, nw, utboard=board[univ - i][time + (i * 2)])
                            for qcx, qcy in qc:
                                moves.append(f"U{univ - i}T{time + (i * 2)}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                    else:
                        break
                    
                n, ne, e, se, s, sw, w, nw = [True for i in range(8)]
                for i in range(1, len(board)):
                    if univ + i < len(board):
                        if len(board[univ + i]) > time + (i * 2) and board[univ + i][time + (i * 2)][0] != ' ':
                            qc = queen_check(x, y, i, n, ne, e, se, s, sw, w, nw, utboard=board[univ + i][time + (i * 2)])
                            for qcx, qcy in qc:
                                moves.append(f"U{univ + i}T{time + (i * 2)}{self.game.rank[qcx]}{qcy + Y_OFFSET}")
                    else:
                        break
            
            elif self.name == "K":

                for i in range(-1, 2):
                    for j in range(-2, 3, 2):
                        if univ + i > -1 and time + j > -1 and univ + i < len(board) and len(board[univ + i]) > time + j and board[univ + i][time + j][0] != ' ':
                            kc = queen_check(x, y, 1, True, True, True, True, True, True, True, True, utboard=board[univ + i][time + j])
                            for kcx, kcy in kc:
                                good_move = True
                                if not att:
                                    for coord in self.attack_lines[f"U{univ + i - self.univ0}T{time + (j if j != 0 else 1)}{self.game.rank[kcx]}{kcy + Y_OFFSET}"]:
                                        if board[coord[0] + self.univ0][coord[1]][coord[2]][coord[3]].color != self.color:
                                            good_move = False
                                            break
                                if good_move:
                                    moves.append(f"U{univ + i}T{time + (j if j != 0 else 1)}{self.game.rank[kcx]}{kcy + Y_OFFSET}")
            
            for i in range(len(moves)): moves[i] = f"U{univ}T{time}{self.game.rank[x]}{y + 1}" + moves[i]
            return moves

    def movePiece(self, board, m):
        black_time_travel = False
        univ, time, x, y, new_univ, new_time, new_x, new_y = self.parse_move(m)

        board[univ].append([board[univ][time][i][:] for i in range(len(board[univ][time]))]) #Copies the previous board into the next time

        new_coords = []
        
        if new_univ != univ and len(board[new_univ]) == new_time + 1: #Traveling to new universe at latest point in its timeline
            board[new_univ].append([board[new_univ][new_time][i][:] for i in range(len(board[new_univ][new_time]))])

            board[new_univ][new_time + 1][new_y][new_x] = board[univ][time][y][x]
            board[univ][time + 1][y][x] = ' '

            new_coords = [new_univ, new_time + 1]

        elif ((new_univ != univ or time + 1 != new_time)
            and board[univ][time][y][x].color == 'W'): # White traveling to a board not at the latest point in time

            board.append([]) #Increments one universe down 
            for i in range(new_time + 1):
                board[len(board) - 1].append(' ')
            board[len(board) - 1].append([board[new_univ][new_time][i][:] for i in range(len(board[new_univ][new_time]))])
            board[len(board) - 1][new_time + 1][new_y][new_x] = board[univ][time][y][x]
            board[univ][time + 1][y][x] = ' '

            new_coords = [len(board) - 1, new_time + 1]

        elif new_univ != univ or time + 1 != new_time: # Black traveling to a board not at the latest point in time
            board.insert(0, []) #Increments one universe up 
            for i in range(new_time + 1):
                board[0].append(' ')
            board[0].append([board[new_univ + 1][new_time][i][:] for i in range(len(board[new_univ + 1][new_time]))])
            board[0][new_time + 1][new_y][new_x] = board[univ + 1][time][y][x]
            board[univ + 1][time + 1][y][x] = ' '
            black_time_travel = True

            self.univ0 += 1
            new_coords = [0, new_time + 1]

        else: # Normal move

            board[new_univ][new_time][new_y][new_x] = board[new_univ][new_time][y][x]
            board[new_univ][new_time][y][x] = ' '

            if ((board[new_univ][new_time][new_y][new_x].name == 'P' and board[new_univ][new_time][new_y][new_x].color == 'W' and new_y == 0)
                or (board[new_univ][new_time][new_y][new_x].name == 'P' and board[new_univ][new_time][new_y][new_x].color == 'B' and new_y == 7)): # change pawn to queen
                board[new_univ][new_time][new_y][new_x].name = 'Q'

            new_coords = [new_univ, new_time]
            
        self.check = []

        turn_done = True
        self.pres_count = 0
        for i in range(len(board)):
            if len(board[i]) <= new_coords[1]:
                turn_done = False
                self.pres_count += 1
        if turn_done:
            self.present = new_coords[1]

        for i in range(8): #add attack lines for board in subsequent time
            for j in range(8):
                piece = board[univ + (1 if black_time_travel else 0)][time + 1][i][j]
                if piece != ' ':
                    if (univ - self.last_univ0, time + 1) not in self.positions:
                        self.positions[(univ - self.last_univ0, time + 1)] = {}
                    if piece.name not in self.positions[(univ - self.last_univ0, time + 1)]:
                        self.positions[(univ - self.last_univ0, time + 1)][piece.name] = [(j, i)]
                    else:
                        self.positions[(univ - self.last_univ0, time + 1)][piece.name].append((j, i))
                    pgm = piece.getMovements(board, f"U{univ + (1 if black_time_travel else 0)}T{time + 1}{self.rank[j]}{i + 1}U{0 + self.univ0}T0a1", att=True)
                    for k in range(len(pgm)):
                        l = pgm[k].find('U', 2) + 1
                        pgm[k] = pgm[k][l - 1] + str(int(pgm[k][l]) - self.last_univ0) + pgm[k][l + 1:]
                        if pgm[k] not in self.attack_lines:
                            self.attack_lines[pgm[k]] = []
                        self.attack_lines[pgm[k]].append((univ - self.last_univ0, time + 1, i, j))
                    self.attacks[(univ - self.last_univ0, time + 1, i, j)] = pgm
                    if piece.name == 'K' and (univ - self.last_univ0, time + 1, i, j) not in self.kings:
                        self.kings.append((univ - self.last_univ0, time + 1, i, j))

        if new_coords != [univ + (1 if black_time_travel else 0), time + 1]: #not a regular move
            for i in range(8): #add attack lines for new board
                for j in range(8):
                    piece = board[new_coords[0]][new_coords[1]][i][j]
                    if piece != ' ':
                        if piece.name == 'K' and (new_coords[0] - self.univ0, new_coords[1], i, j) not in self.kings:
                            self.kings.append((new_coords[0] - self.univ0, new_coords[1], i, j))
                        if (new_coords[0] - self.univ0, new_coords[1]) not in self.positions:
                            self.positions[(new_coords[0] - self.univ0, new_coords[1])] = {}
                        if piece.name not in self.positions[(new_coords[0] - self.univ0, new_coords[1])]:
                            self.positions[(new_coords[0] - self.univ0, new_coords[1])][piece.name] = [(j, i)]
                        else:
                            self.positions[(new_coords[0] - self.univ0, new_coords[1])][piece.name].append((j, i))
                        pgm = piece.getMovements(board, f"U{new_coords[0]}T{new_coords[1]}{self.rank[j]}{i + 1}U{0 + self.univ0}T0a1", att=True)
                        for k in range(len(pgm)):
                            l = pgm[k].find('U', 2) + 1
                            pgm[k] = pgm[k][l - 1] + str(int(pgm[k][l]) - self.univ0) + pgm[k][l + 1:]
                            if pgm[k] not in self.attack_lines:
                                self.attack_lines[pgm[k]] = []
                            self.attack_lines[pgm[k]].append((new_coords[0] - self.univ0, new_coords[1], i, j))
                        self.attacks[(new_coords[0] - self.univ0, new_coords[1], i, j)] = pgm
            self.new_board_att_lines(board, new_coords[0], new_coords[1])
        self.new_board_att_lines(board, univ + (1 if black_time_travel else 0), time + 1)

        del self.positions[(univ - self.last_univ0, time)]
        for i in range(8): #remove attack lines from pieces in old board
            for j in range(8):
                if board[univ + (1 if black_time_travel else 0)][time][i][j] != ' ' and (univ - self.last_univ0, time, i, j) in self.attacks:
                    for space in self.attacks[(univ - self.last_univ0, time, i, j)]:
                        self.attack_lines[space].remove((univ - self.last_univ0, time, i, j))
                        if self.attack_lines[space] == []:
                            del self.attack_lines[space]
                    del self.attacks[(univ - self.last_univ0, time, i, j)]
        if self.last_univ0 == self.univ0 - 1:
            self.last_univ0 += 1
        
        for king in self.kings:
            if f"U{king[0]}T{king[1]}{self.rank[king[3]]}{king[2] + 1}" in self.attack_lines:
                good = True
                for space in self.attack_lines[f"U{king[0]}T{king[1]}{self.rank[king[3]]}{king[2] + 1}"]:
                    if board[space[0] + self.univ0][space[1]][space[2]][space[3]].color != board[king[0] + self.univ0][king[1]][king[2]][king[3]].color:
                        good = False
                        break
                if not good:
                    self.check.append(king)
            if len(board[king[0] + self.univ0]) == king[1] + 1 and f"U{king[0]}T{king[1] + 1}{self.rank[king[3]]}{king[2] + 1}" in self.attack_lines:
                good = True
                for space in self.attack_lines[f"U{king[0]}T{king[1] + 1}{self.rank[king[3]]}{king[2] + 1}"]:
                    if board[space[0] + self.univ0][space[1]][space[2]][space[3]].color != board[king[0] + self.univ0][king[1]][king[2]][king[3]].color:
                        good = False
                        break
                if not good:
                    self.check.append(king)

        return new_coords

    def get_board_state(self):
        return [self.board_array, deepcopy(self.board_array), deepcopy(self.positions), deepcopy(self.attacks), 
                deepcopy(self.attack_lines), deepcopy(self.kings), self.univ0, self.last_univ0, self.present]

    def get_pieces(self):
        result = []

        for i in range(len(self.board_array)):
            for j in range(len(self.board_array[i])):
                for k in range(len(self.board_array[i][j])):
                    for l in range(len(self.board_array[i][j][k])):
                        if self.board_array[i][j][k][l] != ' ':
                            result.append([self.name_array.index(self.board_array[i][j][k][l].name), i, j, k, l])
        
        return result


    def view_board(self, univ, time):
        current_board = self.board_array[univ][time]
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

    def map(self):
        if  self.univ0 > 0:
            print('U |')
        else:
            print('U|')
        for j in range(len(self.board_array)):
            if j - self.univ0 < 0:
                print(f'{j - self.univ0}|',end='')
            else:
                print(f'{j - self.univ0} |',end='')           
            for i in range(len(self.board_array[j])):
                if self.board_array[j][i] == ' ':
                    print('     ',end='')
                else:
                    print(f'[{j},{i}]',end='')
            print()

    def next_turn(self, move=""):
        os.system('clear')

        pres_board_save = deepcopy(self.board_array)
        pos_save = deepcopy(self.positions)
        att_save = deepcopy(self.attacks)
        att_lin_save = deepcopy(self.attack_lines)
        un0_save = self.univ0
        lun0_save = self.last_univ0
        pres_save = self.present

        self.view_board(0,0)
        if move == "":
            move = input("Enter a move: ")
        if move == "map":
            map()
        elif move[0:4] == 'view':
            move = move.split(',')
            self.view_board(int(move[0][-1]), int(move[1][0]))
        else:
            univ, time, x, y, new_univ, new_time, new_x, new_y = self.parse_move(move)
            print(self.board_array[univ][time][y][x].getMovements(self.board_array, move))
            if (self.board_array[univ][time][y][x] == ' ' or
                move not in self.board_array[univ][time][y][x].getMovements(self.board_array, move)): # self.check if legal move
                print("Illegal move!")
            else:
                            
                new_coords = self.movePiece(self.board_array, move)
                
                good = True
                if self.pres_count == 0:
                    for king in self.check:
                        if king[1] <= self.present and self.board_array[king[0] + self.univ0][king[1]][king[2]][king[3]].color == self.board_array[univ + (1 if new_coords == [0, new_time + 1] else 0)][time][y][x].color:
                            good = False
                    if good:
                        pres_board_save = deepcopy(self.board_array)
                        pos_save = deepcopy(self.positions)
                        att_save = deepcopy(self.attacks)
                        att_lin_save = deepcopy(self.attack_lines)
                        self.kings_save = deepcopy(self.kings)
                        un0_save = self.univ0
                        lun0_save = self.last_univ0
                        pres_save = self.present
                        
                        out_of_check_mov = {}
                        mov_len = {}

                        self.check_check = self.check.copy()
                        if len(self.check_check) > 0:
                            self.checkmate = True
                        else:
                            self.checkmate = False

                        for king in self.check_check:
                            if king[1] <= self.present and self.board_array[king[0] + self.univ0][king[1]][king[2]][king[3]].color != self.board_array[univ + (1 if new_coords == [0, new_time + 1] else 0)][time][y][x].color:
                                
                                for i in range(len(self.attack_lines[f"U{king[0]}T{king[1] + (1 if len(self.board_array[king[0] + self.univ0]) == king[1] + 1 else 0)}{self.rank[king[3]]}{king[2] + 1}"])):
                                    attacker = self.attack_lines[f"U{king[0]}T{king[1] + (1 if len(self.board_array[king[0] + self.univ0]) == king[1] + 1 else 0)}{self.rank[king[3]]}{king[2] + 1}"][i]
                                    if self.board_array[attacker[0] + self.univ0][attacker[1]][attacker[2]][attacker[3]].color != self.board_array[king[0] + self.univ0][king[1]][king[2]][king[3]].color:
                                        att_moves = []
                                        if f"U{attacker[0]}T{attacker[1] + (1 if len(self.board_array[attacker[0] + self.univ0]) == attacker[1] + 1 else 0)}{self.rank[attacker[3]]}{attacker[2] + 1}" in self.attack_lines:
                                            for j in range(len(self.attack_lines[f"U{attacker[0]}T{attacker[1] + (1 if len(self.board_array[attacker[0] + self.univ0]) == attacker[1] + 1 else 0)}{self.rank[attacker[3]]}{attacker[2] + 1}"])):
                                                piece = self.attack_lines[f"U{attacker[0]}T{attacker[1] + (1 if len(self.board_array[attacker[0] + self.univ0]) == attacker[1] + 1 else 0)}{self.rank[attacker[3]]}{attacker[2] + 1}"][j]
                                                if self.board_array[piece[0] + self.univ0][piece[1]][piece[2]][piece[3]].color == self.board_array[king[0] + self.univ0][king[1]][king[2]][king[3]].color:
                                                    att_moves += self.board_array[piece[0] + self.univ0][piece[1]][piece[2]][piece[3]].getMovements(self.board_array, f"U{piece[0] + self.univ0}T{piece[1]}{self.rank[piece[3]]}{piece[2] + 1}U0T0a1")

                                        for j in range(len(self.attacks[attacker])):
                                            space = self.attacks[attacker][j]
                                            for k in range(len(self.attack_lines[space])):
                                                piece = self.attack_lines[space][k]
                                                if self.board_array[piece[0] + self.univ0][piece[1]][piece[2]][piece[3]].color == self.board_array[king[0] + self.univ0][king[1]][king[2]][king[3]].color:
                                                    
                                                    for mov in (self.board_array[piece[0] + self.univ0][piece[1]][piece[2]][piece[3]].getMovements(self.board_array, f"U{piece[0] + self.univ0}T{piece[1]}{self.rank[piece[3]]}{piece[2] + 1}U0T0a1") + att_moves):
                                                        temp_board = deepcopy(self.board_array)
                                                        temp_pos = deepcopy(self.positions)
                                                        temp_att = deepcopy(self.attacks)
                                                        temp_att_lin = deepcopy(self.attack_lines)
                                                        temp_self.kings = deepcopy(self.kings)
                                                        temp_un0 = self.univ0
                                                        temp_lun0 = self.last_univ0
                                                        temp_pres = self.present
                                                        
                                                        self.movePiece(self.board_array, mov)

                                                        if len(self.check) == 0:
                                                            print(mov)
                                                            print(self.attack_lines)
                                                            self.checkmate = False

                                                        if king not in self.check:
                                                            if king not in out_of_self.check_mov:
                                                                out_of_self.check_mov[king] = []
                                                            out_of_self.check_mov[king].append(mov)

                                                        self.board_array = deepcopy(temp_board)
                                                        self.positions = deepcopy(temp_pos)
                                                        self.attacks = deepcopy(temp_att)
                                                        self.attack_lines = deepcopy(temp_att_lin)
                                                        self.kings = deepcopy(temp_self.kings)
                                                        self.univ0 = temp_un0
                                                        self.last_univ0 = temp_lun0
                                                        self.present = temp_pres

                                if king not in out_of_self.check_mov:
                                    out_of_self.check_mov[king] = []
                                if len(out_of_self.check_mov[king]) not in mov_len:
                                    mov_len[len(out_of_self.check_mov[king])] = []
                                mov_len[len(out_of_self.check_mov[king])] = king
                        
                        mov_len_keys = list(mov_len.keys())
                        mov_len_keys.sort()
                        mov_len = {i: mov_len[i] for i in mov_len_keys}

                        print(mov_len)

                        if self.checkmate:
                            print("self.checkmate! " + self.board_array[univ + (1 if new_coords == [0, new_time + 1] else 0)][time][y][x].color + " wins!")
                            return self.board_array[univ + (1 if new_coords == [0, new_time + 1] else 0)][time][y][x].color

                if good:
                    self.view_board(new_coords[0], new_coords[1])
                else:
                    self.board_array = deepcopy(pres_board_save)
                    self.positions = deepcopy(pos_save)
                    self.attacks = deepcopy(att_save)
                    self.attack_lines = deepcopy(att_lin_save)
                    self.kings = deepcopy(self.kings_save)
                    self.univ0 = un0_save
                    self.last_univ0 = lun0_save
                    self.present = pres_save

                    rem_list = []
                    for king in self.kings:
                        if king[1] == self.present + 1:
                            rem_list.append(king)
                    for king in rem_list:
                        self.kings.remove(king)

                    self.view_board(univ, time)
                    print("King still in self.check in self.present")


if __name__ == "__main__":
    g = Game()
    while(1):
        g.next_turn()
