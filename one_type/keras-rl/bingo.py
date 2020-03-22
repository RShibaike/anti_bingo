from random import*
import numpy as np


class Bingo:

    def __init__(self):
        self.game_flag = True  # gameが進行中ならTrue
        self.bingo_card = self.make_bingo()
        self.yet_numbers = list(range(1, 76))  # 抽選されていない数のリスト
        self.point = 0

    # ビンゴカードを初期化して作る関数

    def make_bingo(self):
        bingo = [[0 for i in range(5)] for i in range(5)]
        line = [0 for i in range(5)]
        for n in range(5):
            line[n] = list(range(15*n+1, 15*n+16))
        for n in range(5):
            for m in range(5):
                bingo[n][m] = choice(line[m])
                line[m].remove(bingo[n][m])
        bingo[2][2] = 0

        return bingo

    # ビンゴしているかどうか判定する関数

    def isBingo(self):
        checker = False  # Trueならビンゴしている
        # 横列
        for n in self.bingo_card:
            if n.count(0) == 5:
                checker = True
        # line変数初期化
        line = [0 for i in range(5)]
        # 縦列
        for n in range(5):
            for m in range(5):
                line[m] = self.bingo_card[m][n]
            if line.count(0) == 5:
                checker = True
        # 右斜め列
        for n in range(5):
            line[n] = self.bingo_card[n][n]
        if line.count(0) == 5:
            checker = True
        # 左斜め列
        for n in range(5):
            line[n] = self.bingo_card[4-n][n]
        if line.count(0) == 5:
            checker = True

        return checker

    # ポイントを測る関数（ビンゴしていたら当然にゼロ点）

    def isPoint(self):
        counter = 0
        if self.isBingo():
            return 0
        else:
            numbers_of_bingo = []
            for n in self.bingo_card:
                numbers_of_bingo += n
            while 0 in numbers_of_bingo:
                numbers_of_bingo.remove(0)
                counter += 1
            return counter

    # ストップする関数
    def stop(self):
        self.game_flag = False
        self.point = self.isPoint()

    # 1ターン進める関数

    def do_move(self):
        # まだ出ていない数をガラガラ抽選 numberに格納
        number = choice(self.yet_numbers)
        self.yet_numbers.remove(number)

        # でた数の穴を開ける
        for n in range(5):
            if number in self.bingo_card[n]:
                self.bingo_card[n][self.bingo_card[n].index(number)] = 0

        # ビンゴしていたら、gameflagをFalseにして終了
        if self.isBingo:
            self.game_flag = False

    def converter(self, card, turn):
        res = np.array(card)
        res = res.flatten()
        res = np.append(res, turn)
        res = res/75
        return res
