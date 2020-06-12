import random
import numpy as np
from collections import defaultdict, deque
from game import Board, Game
from mcts_alphaZero import MCTSPlayer
from policy_value_net import PolicyValueNet  # Theano and Lasagne
from datetime import datetime
import pickle
import sys
sys.setrecursionlimit(10**8)

class TrainPipeline():
    def __init__(self):
        # 게임(오목)에 대한 변수들
        self.board_width, self.board_height = 9, 9
        self.n_in_row = 5
        self.board = Board(width=self.board_width, height=self.board_height, n_in_row=self.n_in_row)
        self.game = Game(self.board)
        
        # 학습에 대한 변수들
        self.learn_rate = 2e-3
        self.lr_multiplier = 1.0  # KL에 기반하여 학습 계수를 적응적으로 조정
        self.temp = 1.0  # the temperature param
        self.n_playout = 400  # num of simulations for each move
        self.c_puct = 5
        self.buffer_size = 10000
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.batch_size = 512  # mini-batch size : 버퍼 안의 데이터 중 512개를 추출
        self.play_batch_size = 1
        self.epochs = 5  # num of train_steps for each update
        self.kl_targ = 0.02
        self.check_freq = 500  # 지정 횟수마다 모델을 체크하고 저장. 원래는 100이었음.
        self.game_batch_num = 3000  # 최대 학습 횟수
        self.train_num = 0 # 현재 학습 횟수
        
        # policy-value net에서 학습 시작
        self.policy_value_net = PolicyValueNet(self.board_width, self.board_height)
        
        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn, c_puct=self.c_puct, n_playout=self.n_playout, is_selfplay=1)

    def get_equi_data(self, play_data):
        """
        회전 및 뒤집기로 데이터set 확대
        play_data: [(state, mcts_prob, winner_z), ..., ...]
        """
        extend_data = []
        for state, mcts_porb, winner in play_data:
            for i in [1, 2, 3, 4]:
                # 반시계 방향으로 회전
                equi_state = np.array([np.rot90(s, i) for s in state])
                equi_mcts_prob = np.rot90(np.flipud(mcts_porb.reshape(self.board_height, self.board_width)), i)
                extend_data.append((equi_state, np.flipud(equi_mcts_prob).flatten(), winner))
                # 수평으로 뒤집기
                equi_state = np.array([np.fliplr(s) for s in equi_state])
                equi_mcts_prob = np.fliplr(equi_mcts_prob)
                extend_data.append((equi_state, np.flipud(equi_mcts_prob).flatten(), winner))
                
        return extend_data

    def collect_selfplay_data(self, n_games=1):
        """collect self-play data for training"""
        for i in range(n_games):
            winner, play_data = self.game.start_self_play(self.mcts_player, temp=self.temp)
            play_data = list(play_data)[:]
            self.episode_len = len(play_data)
            # 데이터를 확대
            play_data = self.get_equi_data(play_data)
            self.data_buffer.extend(play_data) # deque의 오른쪽(마지막)에 삽입

    def policy_update(self):
        """update the policy-value net"""
        mini_batch = random.sample(self.data_buffer, self.batch_size)
        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]
        old_probs, old_v = self.policy_value_net.policy_value(state_batch)
        for i in range(self.epochs):
            loss, entropy = self.policy_value_net.train_step(state_batch, mcts_probs_batch, winner_batch, self.learn_rate*self.lr_multiplier)
            new_probs, new_v = self.policy_value_net.policy_value(state_batch)
            kl = np.mean(np.sum(old_probs * (np.log(old_probs + 1e-10) - np.log(new_probs + 1e-10)), axis=1))
            
            # D_KL diverges 가 나쁘면 빠른 중지
            if kl > self.kl_targ * 4 : break
                
        # learning rate를 적응적으로 조절
        if kl > self.kl_targ * 2 and self.lr_multiplier > 0.1 : self.lr_multiplier /= 1.5
        elif kl < self.kl_targ / 2 and self.lr_multiplier < 10 : self.lr_multiplier *= 1.5

        explained_var_old = (1 - np.var(np.array(winner_batch) - old_v.flatten()) / np.var(np.array(winner_batch)))
        explained_var_new = (1 - np.var(np.array(winner_batch) - new_v.flatten()) / np.var(np.array(winner_batch)))

        print(f"kl:{kl:5f}, lr_multiplier:{self.lr_multiplier:3f}, loss:{loss}, entropy:{entropy}, explained_var_old:{explained_var_old:3f}, explained_var_new:{explained_var_new:3f}")

        return loss, entropy

    def run(self):
        for i in range(self.game_batch_num):
            self.collect_selfplay_data(self.play_batch_size)
            self.train_num += 1
            print(f"batch i:{self.train_num}, episode_len:{self.episode_len}")

            if len(self.data_buffer) > self.batch_size : loss, entropy = self.policy_update()

            # 현재 model의 성능을 체크, 모델 속성을 저장
            if (i+1) % self.check_freq == 0:
                print(f"★ {self.train_num}번째 batch에서 모델 저장 : {datetime.now()}")
                self.policy_value_net.save_model(f'{model_path}/policy_9_{self.train_num}.model')
                pickle.dump(self, open(f'{train_path}/train_9_{self.train_num}.pickle', 'wb'), protocol=2)

if __name__ == '__main__':
    print("9x9 환경에서 학습을 진행합니다.")
    train_path = f"./save/train_9"
    model_path = f"./save/model_9"
    
    init_num = int(input('현재까지 저장된 모델의 학습 수 : '))
    if init_num == 0 or init_num == None : training_pipeline = TrainPipeline()
    else : training_pipeline = pickle.load(open(f'{train_path}/train_9_{init_num}.pickle', 'rb'))

    print(f"★ 학습시작 : {datetime.now()}")
    training_pipeline.run()
    