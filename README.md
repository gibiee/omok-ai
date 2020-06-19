[알파고(AlphaGo)](https://www.nature.com/articles/nature16961)와 [알파고 제로(AlphaGo Zero)](https://www.nature.com/articles/nature24270)의 방법론을 모방하여 오목 인공지능(AI)을 구현하는 프로젝트입니다.

아래 유사 프로젝트들의 소스코드를 적극 활용하였습니다.
- [An implementation of the AlphaZero algorithm for Gomoku](https://github.com/junxiaosong/AlphaZero_Gomoku)
- [렌주룰 판별](https://blog.naver.com/dnpc7848/221506783416)

## 프로젝트 실행 과정
실행 과정은 학습(train)과 플레이(play) 두 과정으로 구분됩니다.
- 학습(train)
  - 딥러닝을 활용한 학습을 반복하여 모델(model)을 생성합니다.
  - 과정 생략 가능. (model 폴더에 이미 생성된 모델이 저장되어 있음)
- 플레이(play)
  - 플레이어(사람)은 학습된 모델을 기반으로 하는 AI(인공지능)와 오목을 플레이할 수 있습니다.
  - 오목 인공지능은 9x9 환경에서 동작합니다.
  - :star:**플레이 하는 방법**:star:
  - [play.ipynb](https://github.com/gibiee/omok_AI/blob/master/play.ipynb)에서 "Open in Colab" 버튼을 통해 Google Colab 환경에서 플레이할 수 있습니다. [[Direct Link](https://colab.research.google.com/github/gibiee/omok_AI/blob/master/play.ipynb)]
  - 입력 예시   
  <img src="https://user-images.githubusercontent.com/37574274/81725519-eb44ae80-94c0-11ea-97a3-ee944e50af2b.png" width="80%"></img>


## 방법론
사용한 주요 방법론은 다음과 같이 3가지입니다.
- 정책망(Policy Network)
  - 알파고(AlphaGo)에서 사용된 방법론으로, 현재 오목판의 상태(state)를 입력받아 각 위치에 대한 기댓값을 계산합니다.
  - 기댓값이 크다는 것은 자신 또는 상대가 착수하기 좋은 위치를 의미합니다.
- 자가 대국(self-play)을 통한 학습
  - 알파고 제로(AlphaGo Zero)에서 사용된 방법론으로, 자가 대국을 통해서 생성한 플레이 데이터만을 사용하여 정책망을 학습합니다.
  - 인간의 플레이 데이터를 전혀 사용하지 않았음에도, 알파고 제로는 알파고보다 뛰어난 성능을 보여주었습니다.
- MCTS(Monte Carlo Tree Search : 몬테카를로 트리 탐색) 알고리즘
  - 알파고와 알파고 제로에서 사용된 방법론으로, 다양한 경우의 수를 탐색하여 최종적으로 착수 위치를 결정합니다.

## 각 구성 파일들의 역할
|파일명|구분|설명|
|------|:---:|----|
|game.py|공통|오목 게임의 규칙을 정의합니다.|
|renju_rule.py|공통|렌주룰의 규칙을 정의합니다.|
|mcts_alphaZero.py|공통|MCTS 알고리즘을 정의합니다.|
|train.py|학습|정책망의 학습 과정을 반복 진행합니다.<br/>100번 반복할 때마다 모델을 파일 형태로 저장합니다.|
|policy_value_net.py|학습|정책망의 구조를 정의합니다. Theano 라이브러리를 사용합니다.|
|human_play.py|플레이|사람과 AI의 대결을 실행합니다.|
|policy_value_net_numpy.py|플레이|저장된 모델 파일을 불러옵니다. numpy 라이브러리를 사용합니다.|

## 한계
- 정책망의 학습 횟수가 증가한다고 해서, 성능이 선형적으로 증가하지는 않음.
- 15x15 환경에서는 학습에 소요되는 시간이 매우 큼. 그리고 학습에 소요된 시간에 비해 성능이 기대에 못 미침.

## 참고 자료
전체적인 배경을 파악하는데 유용합니다.
- [알파고 - 나무위키](https://namu.wiki/w/%EC%95%8C%ED%8C%8C%EA%B3%A0)
- [오목(렌주룰) - 나무위키](https://namu.wiki/w/%EC%98%A4%EB%AA%A9?from=%EC%98%A4%EB%AA%A9%28%EA%B2%8C%EC%9E%84%29#s-2.3)

이론적으로 참고한 자료들입니다.
- [강화학습의 개념](https://jeinalog.tistory.com/20)
- [DQN과 Policy Gradient의 차이](https://gist.github.com/ByungSunBae/56009ed6ea31bb91a236e67bcb3245a2)
- [DQN과 Policy Gradient의 차이(2)](https://dnddnjs.gitbooks.io/rl/content/numerical_methods.html)
- [Minimax 알고리즘과 MCTS 알고리즘](https://shuuki4.wordpress.com/2016/03/11/alphago-alphago-pipeline-%ED%97%A4%EC%A7%91%EA%B8%B0/)
- [알파고 논문 번역](https://blog.naver.com/sogangori/220668124217)
- [알파고에 적용된 딥러닝 알고리즘 분석](https://brunch.co.kr/@justinleeanac/2)
- [알파고 제로 분석(MCTS)](https://leekh7411.tistory.com/1?category=768501)
- [알파고 제로와 알파제로에 대한 분석](https://jsideas.net/AlphaZero/)
