from __future__ import print_function
import pickle
from game import Board, Game
# from mcts_pure import MCTSPlayer as MCTS_Pure    # 순수 MCTS
from mcts_alphaZero import MCTSPlayer           # 변형된 MCTS
from policy_value_net_numpy import PolicyValueNetNumpy # numpy

class Human(object):
    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("돌을 둘 좌표를 입력 : ")
            if isinstance(location, str) : location = [int(n, 10) for n in location.split(",")]
            location = [value-1 for value in location]
            move = board.location_to_move(location)
        except Exception as e : move = -1
            
        if move == -1 or move not in board.availables or (board.is_you_black() and tuple(location) in board.forbidden_locations) :
            print("다시 입력하십시오.")
            move = self.get_action(board)
            
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    n = 5
    width, height = 8, 8
    # width, height = 15, 15
    model_file = './model/best_policy_8_8_5.model'
    # model_file = './model/policy_100.model'
    
    board = Board(width=width, height=height, n_in_row=n)
    game = Game(board)

    # 이미 제공된 model을 불러와서 pure numpy로 작성된 MCTS player에 넣는다.
    try: policy_param = pickle.load(open(model_file, 'rb'))
    except: policy_param = pickle.load(open(model_file, 'rb'), encoding='bytes')

    # 학습된 policy_value_net를 불러온다.
    best_policy = PolicyValueNetNumpy(width, height, policy_param)
    mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)  # n_playout 값이 커지면 성능이 좋아짐
    # pure MCTS를 사용하려면 아래 줄을 사용 (더 큰 n_playout 값으로도 성능이 약함.)
    # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

    human = Human()
    # human2 = Human()
    
    # start_player=0 → 사람 선공
    # start_player=1 → AI 선공
    game.start_play(human, mcts_player, start_player=1, is_shown=1)   
    
    # game.start_play(human, human2, start_player=0, is_shown=1)


if __name__ == '__main__':
    run()
