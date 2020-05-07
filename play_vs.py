import pickle
from game import Board, Game
from mcts_alphaZero1 import MCTSPlayer as MCTSPlayer1 # 확률론적
from mcts_alphaZero2 import MCTSPlayer as MCTSPlayer2 # 결정론적
from policy_value_net_numpy import PolicyValueNetNumpy

class Human(object):
    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("돌을 둘 좌표를 입력 : ")
            if isinstance(location, str) : location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e : move = -1
            
        if move == -1 or move in board.states.keys() :
            print("다시 입력하십시오.")
            move = self.get_action(board)
        elif board.is_you_black() and tuple(location) in board.forbidden_locations :
            print("금수 자리에 돌을 놓을 수 없습니다.")
            move = self.get_action(board)
            
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    n = 5
    width, height = 9, 9
    
    board = Board(width=width, height=height, n_in_row=n)
    game = Game(board)

    policy_param1 = pickle.load(open('./omok_AI/model/policy_9_9_10000.model', 'rb'), encoding='bytes')
    best_policy1 = PolicyValueNetNumpy(width, height, policy_param1)
    mcts_player1 = MCTSPlayer1(best_policy.policy_value_fn, c_puct=5, n_playout=400) # n_playout값 : 성능

    policy_param2 = pickle.load(open('./omok_AI/model/policy_9_9_10000.model', 'rb'), encoding='bytes')
    best_policy2 = PolicyValueNetNumpy(width, height, policy_param2)
    mcts_player2 = MCTSPlayer2(best_policy.policy_value_fn, c_puct=5, n_playout=400) # n_playout값 : 성능
    
    print("mcts_player1 : 10000")
    print("mcts_player2 : 10000")
    game.start_play(mcts_player1, mcts_player2, start_player=0, is_shown=1)   

if __name__ == '__main__':
    run()