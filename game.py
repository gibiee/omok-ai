# -*- coding: utf-8 -*-
import numpy as np
from renju_rule import Renju_Rule
from IPython.display import clear_output
import os

class Board(object):
    def __init__(self, **kwargs):
        self.width = int(kwargs.get('width', 15))
        self.height = int(kwargs.get('height', 15))
        self.n_in_row = int(kwargs.get('n_in_row', 5))
        self.players = [1, 2]  # player1 and player2

    def init_board(self, start_player=0) :
        self.order = start_player # order = 0 → 사람 선공(흑돌) / 1 → AI 선공(흑돌)
        self.current_player = self.players[start_player]  # current_player = 1 → 사람 / 2 → AI
        self.last_move, self.last_loc = -1, -1
        
        self.states, self.states_loc = {}, [[0] * self.width for _ in range(self.height)]
        self.forbidden_locations, self.forbidden_moves = [], []
        
        """금수 판정 디버그용
        self.states = {32:1, 47:1, 63:1, 64:1}
        self.states_loc = list(
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] )"""

    def move_to_location(self, move):
        """ 3*3 보드를 예로 들면 : move 5 는 좌표 (1,2)를 의미한다.
        0 1 2
        3 4 5
        6 7 8
        """
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2 : return -1
        h, w = location[0], location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height) : return -1
        return move

    def current_state(self):
        """현재 플레이어의 관점에서 보드 상태(state)를 return한다.
        state shape: 4 * [width*height]
        """
        square_state = np.zeros((4, self.width, self.height))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]
            square_state[0][move_curr // self.width, move_curr % self.height] = 1.0 #내가 둔 돌의 위치를 1로 표현
            square_state[1][move_oppo // self.width, move_oppo % self.height] = 1.0 #적이 둔 돌의 위치를 1로 표현
            square_state[2][self.last_move // self.width, self.last_move % self.height] = 1.0 #마지막 돌의 위치
            
        if len(self.states) % 2 == 0 : square_state[3][:, :] = 1.0  # indicate the colour to play
        
        print(square_state)
        return square_state[:, ::-1, :]

    def do_move(self, move):
        self.states[move] = self.current_player
        loc = self.move_to_location(move)
        self.states_loc[loc[0]][loc[1]] = 1 if self.is_you_black() else 2
        self.current_player = (self.players[0] if self.current_player == self.players[1] else self.players[1])
        self.last_move, self.last_loc = move, loc

    def has_a_winner(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row

        # moved : 이미 돌이 놓인 자리들
        moved = list(self.states.keys())
        if len(moved) < self.n_in_row * 2-1 : return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player
        
        return False, -1

    def game_end(self):
        win, winner = self.has_a_winner()
        if win : return True, winner
        elif len(self.states) == self.width*self.height : return True, -1
        return False, -1

    def get_current_player(self):
        return self.current_player
    
    def set_forbidden(self) :
        # forbidden_locations : 흑돌 기준에서 금수의 위치
        rule = Renju_Rule(self.states_loc, self.width)
        self.forbidden_locations = rule.get_forbidden_points(stone=1)
        self.forbidden_moves = [self.location_to_move(loc) for loc in self.forbidden_locations]
        
    def is_you_black(self) :
        # order, current_player
        # (0,1) → 사람(흑돌)
        # (0,2) → AI(백돌)
        # (1,1) → 사람(백돌)
        # (1,2) → AI(흑돌)
        if self.order == 0 and self.current_player == 1 : return True
        elif self.order == 1 and self.current_player == 2 : return True
        else : return False

class Board_9_9(Board) :
    def __init__(self, board) :
        self.width, self.height, self.n_in_row = 9, 9, 5
        self.order, self.current_player = board.order, board.current_player
        self.forbidden_locations, self.forbidden_moves = [], []
        self.players = board.players
        self.last_move, self.last_loc = board.last_move, board.last_loc
        
        if board.last_loc == -1 : last_y, last_x = 7,7
        else : last_y, last_x = board.last_loc
           
        if last_y <= 4 : y1, y2 = 0,8
        elif 5 <= last_y <= 9 : y1, y2 = last_y-4, last_y+4
        else : y1, y2 = 6,14
            
        if last_x <= 4 : x1, x2 = 0,8
        elif 5 <= last_x <= 9 : x1, x2 = last_x-4, last_x+4
        else : x1, x2 = 6,14

        self.bias_y, self.bias_x = y1, x1
        self.states = {}
        self.states_loc = np.array(board.states_loc)[y1:y2+1, x1:x2+1].tolist()
        
        print("원래 보드")
        print(np.array(board.states_loc))
        print("자른보드", y1,y2,x1,x2)
        print(np.array(self.states_loc))
        
        m = 0
        player = [[1,2],[2,1]]
        for y in range(9) :
            for x in range(9) :
                if self.states_loc[y][x] == 1 : self.states[m] = player[board.order][0]
                elif self.states_loc[y][x] == 2 : self.states[m] = player[board.order][1]
                m += 1
                    
        print(f"보드 states = {board.states}")
        print(f"자른 states = {self.states}")
        
        # 금수가 자른 보드 9x9 내에 있는지 확인
        for locY, locX in board.forbidden_locations :
            if y1 <= locY <= y2 and x1 <= locX <= x2 :
                f_loc = (locY - y1, locX - x1)
                self.forbidden_locations.append(f_loc)
                self.forbidden_moves = self.location_to_move(self.forbidden_locations)
        
        print(f"보드 f_loc = {board.forbidden_locations}")
        print(f"자른 f_loc = {self.forbidden_locations}")
        
        print(f"보드 f_moves = {board.forbidden_moves}")
        print(f"자른 f_moves = {self.forbidden_moves}")

class Game(object):
    def __init__(self, board, **kwargs):
        self.board = board

    def graphic(self, board, player1, player2):
        width = board.width
        height = board.height

        # clear_output(wait=True)
        # os.system('cls')
        
        print()
        if board.order == 0 : 
            print("흑돌(●) : 플레이어")
            print("백돌(○) : AI")
        else :
            print("흑돌(●) : AI")
            print("백돌(○) : 플레이어")
        print("--------------------------------\n")
        
        if board.current_player == 1 : print("당신의 차례입니다.\n")
        else : print("AI가 수를 두는 중...\n")
            
        row_number = ['⒪','⑴','⑵','⑶','⑷','⑸','⑹','⑺','⑻','⑼','⑽','⑾','⑿','⒀','⒁']
        print('　', end='')
        for i in range(height) : print(row_number[i], end='')
        print()
        for i in range(height):
            print(row_number[i], end='')
            for j in range(width):
                loc = i * width + j
                p = board.states.get(loc, -1)
                if p == player1 : print('●' if board.order == 0 else '○', end='')
                elif p == player2 : print('○' if board.order == 0 else '●', end='')
                elif board.is_you_black() and (i,j) in board.forbidden_locations : print('Ⅹ', end='')
                else : print('　', end='')
            print()
        if board.last_loc != -1 :
            print(f"마지막 돌의 위치 : ({board.last_loc[0]},{board.last_loc[1]})\n")

    def start_play(self, player1, player2, start_player=0, is_shown=1):
        self.board.init_board(start_player)
        p1, p2 = self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2: player2}
        while True:
            # 흑돌일 때, 금수 위치 확인하기
            if self.board.is_you_black() : self.board.set_forbidden()
            if is_shown : self.graphic(self.board, player1.player, player2.player)
                
            current_player = self.board.get_current_player()
            player_in_turn = players[current_player]
            # test = Board_9_9(self.board)
            # move = player_in_turn.get_action(test) # 추후에 bias 적용할것
            move = player_in_turn.get_action(self.board)
            self.board.do_move(move)
            end, winner = self.board.game_end()
            if end:
                if is_shown:
                    self.graphic(self.board, player1.player, player2.player)
                    if winner != -1 : print("Game end. Winner is", players[winner])
                    else : print("Game end. Tie")
                return winner

    def start_self_play(self, player, is_shown=0, temp=1e-3):
        """ 스스로 자가 대국하여 학습 데이터(state, mcts_probs, z) 생성 """
        self.board.init_board()
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []
        while True:
            # 흑돌일 때, 금수 위치 확인하기
            if self.board.is_you_black() : self.board.set_forbidden()
            if is_shown : self.graphic(self.board, p1, p2)
                
            move, move_probs = player.get_action(self.board, temp=temp, return_prob=1)
            # store the data
            states.append(self.board.current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.current_player)
            
            # perform a move
            self.board.do_move(move)
                
            end, winner = self.board.game_end()
            if end:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                # reset MCTS root node
                player.reset_player()
                if is_shown:
                    self.graphic(self.board, p1, p2)
                    if winner != -1 : print("Game end. Winner is player:", winner)
                    else : print("Game end. Tie")
                return winner, zip(states, mcts_probs, winners_z)
