from __future__ import print_function
import pickle
from game import Board, Game
#from mcts_pure import MCTSPlayer as MCTS_Pure    # 순수 MCTS
from mcts_alphaZero import MCTSPlayer           # 변형된 MCTS
from policy_value_net_numpy import PolicyValueNetNumpy
# from policy_value_net import PolicyValueNet  # Theano and Lasagne
# from policy_value_net_pytorch import PolicyValueNet  # Pytorch
# from policy_value_net_tensorflow import PolicyValueNet # Tensorflow
# from policy_value_net_keras import PolicyValueNet  # Keras

class Human(object):

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str) : location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e : move = -1
            
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
            
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    n = 5
    width, height = 8, 8
    model_file = 'best_policy_8_8_5.model'
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)

        # 학습된 policy_value_net를 불러온다. (Theano/Lasagne, PyTorch or TensorFlow)
        # best_policy = PolicyValueNet(width, height, model_file = model_file)
        # mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy
        try: policy_param = pickle.load(open(model_file, 'rb'))
        except: policy_param = pickle.load(open(model_file, 'rb'), encoding='bytes')
            
        best_policy = PolicyValueNetNumpy(width, height, policy_param)
        mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)  # n_playout 값이 커지면 성능이 좋아짐

        # pure MCTS를 사용하려면 아래 줄을 사용 (더 큰 n_playout 값으로도 성능이 약함.)
        # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human()

        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=1, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
