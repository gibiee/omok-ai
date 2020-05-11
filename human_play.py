import pickle
from game import Board, Game
from mcts_alphaZero import MCTSPlayer
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
    # width, height = 15, 15
    # model_file = './model/policy_5000.model'
    width, height = 9, 9
    # model_file = './model/policy_9_9_10000.model'
    model_file = '.omok_AI/model/policy_9_9_10000.model'
    
    board = Board(width=width, height=height, n_in_row=n)
    game = Game(board)

    # 이미 제공된 model을 불러와서 학습된 policy_value_net을 얻는다.
    policy_param = pickle.load(open(model_file, 'rb'), encoding='bytes')
    best_policy = PolicyValueNetNumpy(width, height, policy_param)
    
    mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400) # n_playout값 : 성능
    
    human = Human()
    # human2 = Human()
    
    # start_player=0 → 사람 선공
    # start_player=1 → AI 선공
    game.start_play(human, mcts_player, start_player=0, is_shown=1)   
    
    # game.start_play(human, human2, start_player=0, is_shown=1)

if __name__ == '__main__':
    run()