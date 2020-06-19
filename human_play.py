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
            print("돌을 둘 좌표를 입력하세요.")
            location = input()
            if isinstance(location, str) : location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e : move = -1
            
        if move == -1 or move in board.states.keys() :
            print("다시 입력하세요.")
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
    print("이 오목 인공지능은 9x9 환경에서 동작합니다.")
    
    print("현재 가능한 난이도(정책망의 학습 횟수) 목록 : [ 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000 ]")
    print("난이도를 입력하세요.")
    hard = int(input())
    model_file = f'./omok_AI/model/policy_9_{hard}.model'    # colab
    # model_file = f'./model/policy_9_{hard}.model'          # local
    
    print("자신이 선공(흑)인 경우에 0, 후공(백)인 경우에 1을 입력하세요.")
    order = int(input())
    if order not in [0,1] : return "강제 종료"

    board = Board(width=width, height=height, n_in_row=n)
    game = Game(board)

    # 이미 제공된 model을 불러와서 학습된 policy_value_net을 얻는다.
    policy_param = pickle.load(open(model_file, 'rb'), encoding='bytes')
    best_policy = PolicyValueNetNumpy(width, height, policy_param)
    
    mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400) # n_playout값 : 성능
    human = Human()
    
    # start_player = 0 → 사람 선공 / 1 → AI 선공
    game.start_play(human, mcts_player, start_player=order, is_shown=1)

if __name__ == '__main__':
    run()