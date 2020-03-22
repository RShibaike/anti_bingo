import gym
import gym.spaces
import numpy as np
from bingo import Bingo

# 直線上を動く点の速度を操作し、目標(原点)に移動させることを目標とする環境


class PointOnLine(gym.core.Env):
    def __init__(self):
        bingo = Bingo()
        self.action_space = gym.spaces.Discrete(2)  # 行動空間。ストップorしない
        high = [1 for i in range(26)]
        high = np.array(high)
        low = [0 for i in range(26)]
        low = np.array(low)
        self.observation_space = gym.spaces.Box(
            low=low, high=high)  # 観測空間(state)の次元 (26) とそれらの最大値(1)、最小値(0)

    # 各stepごとに呼ばれる
    # actionを受け取り、次のstateとreward、episodeが終了したかどうかを返すように実装
    def _step(self, action):
        # actionを受け取り、次のstateを決定
        if action == 1:
            bingo.stop()
        else:
            bingo.do_move()

        # 位置と速度の絶対値が十分小さくなったらepisode終了
        done = not(bingo.game_flag)

        if done:
            # 終了したときに正の報酬
            reward = isPoint()

        # 次のstate、reward、終了したかどうか、追加情報の順に返す
        # 追加情報は特にないので空dict
        return bingo.converter(bingo.bingo_card, len(bingo.yet_numbers)), reward, done, {}

    # 各episodeの開始時に呼ばれ、初期stateを返すように実装
    def _reset(self):
        # 初期stateは、位置はランダム、速度ゼロ
        bingo.bingo_card = bingo.make_bingo()
        bingo.yet_numbers = list(range(1, 76))  # 抽選されていない数のリスト
        return bingo.converter(bingo.bingo_card, len(bingo.yet_numbers))
