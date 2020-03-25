import sys
from fractions import Fraction
import math
import random
import time
import copy
import itertools
import sys
from operator import itemgetter
import statistics as st
import statistics
import copy
import pandas as pd


# 穴を開ける関数
# x:番号, y:ビンゴの局面
def open_bingo(x, y):
    for n in range(5):
        if x in y[n]:
            y[n][y[n].index(x)] = 0


# nマス連続で空いている箇所が何箇所ある判定する関数
# x:ビンゴの局面, y:nマス, return:そこあけるとビンゴになる数のリスト
def reach(x, y):
    # counter変数初期化
    counter = []
    # 横列
    for n in x:
        if n.count(0) == y:
            counter += n
    # line変数初期化
    line = [0 for i in range(5)]
    # 縦列
    for n in range(5):
        for m in range(5):
            line[m] = x[m][n]
        if line.count(0) == y:
            counter += line
    # 右斜め列
    for n in range(5):
        line[n] = x[n][n]
    if line.count(0) == y:
        counter += line
    # 左斜め列
    for n in range(5):
        line[n] = x[4-n][n]
    if line.count(0) == y:
        counter += line
    # 0削除
    while 0 in counter:
        counter.remove(0)

    return counter


# ビンゴしてるかどうか調べてくれる関数
# x:ビンゴの局面, return:ビンゴしてたら１、してないと０
def bingo(x):
    # counter変数初期化
    counter = 0
    # 横列
    for n in x:
        if n.count(0) == 5:
            counter = 1
    # line変数初期化
    line = [0 for i in range(5)]
    # 縦列
    for n in range(5):
        for m in range(5):
            line[m] = x[m][n]
        if line.count(0) == 5:
            counter = 1
    # 右斜め列
    for n in range(5):
        line[n] = x[n][n]
    if line.count(0) == 5:
        counter = 1
    # 左斜め列
    for n in range(5):
        line[n] = x[4-n][n]
    if line.count(0) == 5:
        counter = 1

    return counter


# 現在の得点を測る（空いてるマス数を数える）関数
# ビンゴしてたらちゃんとゼロになる
# x:ビンゴの局面, return:得点
def point(x):
    counter = 0
    if bingo(x) == 1:
        return 0
    else:
        numbers_of_bingo = []
        for n in x:
            numbers_of_bingo += n
        while 0 in numbers_of_bingo:
            numbers_of_bingo.remove(0)
            counter += 1
        return counter


# 期待値だしてくれる関数
# x:ビンゴの局面, y:まだ出てない数字, return:期待値
def expected_value(x, y):
    return (25-point(x))/len(y)-len(reach(x, 4))/len(y)*point(x)


# ビンゴを書き出してくれる関数
# x:ビンゴの局面
def output(x):
    op = [[[0 for i in range(5)] for j in range(5)] for k in range(4)]
    for k in range(4):
        for i in range(5):
            for j in range(5):
                op[k][i][j] = str(x[k][i][j])
                if(0 <= int(op[k][i][j]) <= 9):
                    op[k][i][j] = "0"+op[k][i][j]
            a = str(op[k][i])
            a = a.replace(",", "")
            a = a.replace("'", "")
            a = a.strip("[")
            a = a.strip("]")
            print(a)
        print("-----------------")


# positions(ビンゴカードの盤面), stopflags（ストップされてるかどうかのフラグ）,
# points（前のポイントを取得するのに使う）, position_value（空いてる箇所による点数）,
# position_point（穴の数、２、３、４連続の箇所の数にかける係数）, how_stop（前の点数に対していつとめるか）
# return 次のあるべきstop_flags
def evaluation_function(positions, stopflags, points, position_value, position_point, how_stop):
    value = [0, 0, 0, 0]

    for i in range(4):
        if stopflags[i] == 0:
            for j in range(5):
                for k in range(5):
                    if positions[i][j][k] == 0:
                        if j == 2 and k == 2:
                            value[i] += 10
                            # print("b")
                        if (j, k) in [(1, 2), (2, 1), (3, 2), (2, 3)]:
                            value[i] += position_value[0]
                        if (j, k) in [(1, 1), (1, 3), (3, 1), (3, 3)]:
                            value[i] += position_value[1]
                        if (j, k) in [(0, 2), (2, 0), (2, 4), (4, 2)]:
                            value[i] += position_value[2]
                        if (j, k) in [(0, 1), (0, 3), (1, 0), (1, 4), (3, 0), (3, 4), (4, 1), (4, 3)]:
                            value[i] += position_value[3]
                        if (j, k) in [(0, 0), (0, 4), (4, 0), (4, 4)]:
                            value[i] += position_value[4]
            value[i] += (position_point[0]*point(positions[i])
                         + position_point[1]*len(reach(positions[i], 2))
                         + position_point[2]*len(reach(positions[i], 3))
                         + position_point[3]*len(reach(positions[i], 4)))
    counter = 0
    return_stopflags = copy.copy(stopflags)

    for i in range(4):
        if stopflags[i] == 0 and point(positions[i]) == 20:
            return_stopflags[i] = 1
            counter += 1

        elif stopflags[i] == 0 and point(positions[i]) > 4 and value[i] > how_stop[points[-1] - 5 + counter]:
            return_stopflags[i] = 1
            counter += 1

    return return_stopflags


# 長さ：3480960000

# def board_to_q_number(board, turn, stop, act):
#     res = turn*46412800
#     res += stop*2900800
#     res += len(reach(board, 2))*59200
#     res += len(reach(board, 3))*1600
#     res += len(reach(board, 4))*64
#     res += len(reach(board, 5))*4
#     res += act
#     res -= 1
#     return res

# def number_to_stopflag(number):
#     res = [0, 0, 0, 0]
#     for i in range(4):
#         res[3-i] = number % 2
#         number = number//2
#     return res


def number_to_stopflag(number):
    if number == 0:
        return [0, 0, 0, 0]
    if number == 1:
        return [0, 0, 0, 1]
    if number == 2:
        return [0, 0, 1, 0]
    if number == 3:
        return [0, 1, 0, 0]
    if number == 4:
        return [1, 0, 0, 0]
    # if number == 5:
    #     return [0, 0, 1, 1]
    # if number == 6:
    #     return [0, 1, 0, 1]
    # if number == 7:
    #     return [1, 0, 0, 1]
    # if number == 8:
    #     return [0, 1, 1, 0]
    # if number == 9:
    #     return [1, 0, 1, 0]
    # if number == 10:
    #     return [1, 1, 0, 0]
    # if number == 11:
    #     return [0, 1, 1, 1]
    # if number == 12:
    #     return [1, 0, 1, 1]
    # if number == 13:
    #     return [1, 1, 0, 1]
    # if number == 14:
    #     return [1, 1, 1, 0]
    # if number == 15:
    #     return [1, 1, 1, 1]


def stopflag_to_number(flag):
    if flag == [0, 0, 0, 0]:
        return 0
    if flag == [0, 0, 0, 1]:
        return 1
    if flag == [0, 0, 1, 0]:
        return 2
    if flag == [0, 1, 0, 0]:
        return 3
    if flag == [1, 0, 0, 0]:
        return 4
    # if flag == [0, 0, 1, 1]:
    #     return 5
    # if flag == [0, 1, 0, 1]:
    #     return 6
    # if flag == [1, 0, 0, 1]:
    #     return 7
    # if flag == [0, 1, 1, 0]:
    #     return 8
    # if flag == [1, 0, 1, 0]:
    #     return 9
    # if flag == [1, 1, 0, 0]:
    #     return 10
    # if flag == [0, 1, 1, 1]:
    #     return 11
    # if flag == [1, 0, 1, 1]:
    #     return 12
    # if flag == [1, 1, 0, 1]:
    #     return 13
    # if flag == [1, 1, 1, 0]:
    #     return 14
    # if flag == [1, 1, 1, 1]:
    #     return 15


def number_to_str(number):
    number = str(number)
    if len(number) == 1:
        number = "0"+number
    return number


# 入力：stop_flags:[0,1,2,0], point:[13,0],
# l2:[6,5,5,4], l3:[4,5,4,3], l4:[2,3,4,5], act[1,0,0,1]
# 出力："012013000000386554454323451001"
# board_to_str([0, 1, 2, 0], [13, 0], [6, 5, 5, 4],
#              [4, 5, 4, 3], [2, 3, 4, 5], [1, 0, 0, 1])

def board_to_str(stop_flags, point, l2, l3, l4, act):
    res = ""
    for i in stop_flags:
        res += str(i)
    res += str(point)
    for i in l2:
        if i >= 5:
            i = 4
        res += str(i)
    for i in l3:
        if i >= 5:
            i = 4
        res += str(i)
    for i in l4:
        if i >= 5:
            i = 4
        res += str(i)
    for i in act:
        res += str(i)
    return res


def babble_sort_index(ar):
    """ バブルソート """
    arr = copy.copy(ar)
    length = len(arr)
    index = [i for i in range(length)]
    for i in range(length):
        # 3. 走査範囲を前からひとつ狭める
        for j in reversed(range(i+1, length)):
            # 1. 後ろから順に隣り合う要素を比較する。
            if arr[j-1] > arr[j]:
                # 2. 左が右の要素に比べ大きい場合交換する。
                arr[j-1], arr[j], index[j -
                                        1], index[j] = arr[j], arr[j-1], index[j], index[j-1]
    return index


def positions_sort(stop_flags, l2, l3, l4, act):
    r0 = [i for i, x in enumerate(stop_flags) if x == 0]
    r1 = [i for i, x in enumerate(stop_flags) if x == 1]
    r2 = [i for i, x in enumerate(stop_flags) if x == 2]
    if len(r0) != 1:
        l2r = []
        for i in r0:
            l2r.append(l2[i])
        l2r2 = babble_sort_index(l2r)
        r02 = copy.copy(r0)
        for i in range(len(r0)):
            r0[i] = r02[l2r2[i]]
    if len(r1) != 1:
        l2r = []
        for i in r1:
            l2r.append(l2[i])
        l2r2 = babble_sort_index(l2r)
        r12 = copy.copy(r1)
        for i in range(len(r1)):
            r1[i] = r12[l2r2[i]]
    if len(r2) != 1:
        l2r = []
        for i in r2:
            l2r.append(l2[i])
        l2r2 = babble_sort_index(l2r)
        r22 = copy.copy(r2)
        for i in range(len(r2)):
            r2[i] = r22[l2r2[i]]
    res = r0 + r1 + r2
    res_stopflags = copy.copy(stop_flags)
    res_l2 = copy.copy(l2)
    res_l3 = copy.copy(l3)
    res_l4 = copy.copy(l4)
    res_act_stopflags = number_to_stopflag(act)

    for i in range(4):
        res_stopflags[i] = stop_flags[res[i]]
        res_l2[i] = l2[res[i]]
        res_l3[i] = l3[res[i]]
        res_l4[i] = l4[res[i]]
        res_act_stopflags[i] = number_to_stopflag(act)[res[i]]

    res_act = stopflag_to_number(res_act_stopflags)

    return res_stopflags, res_l2, res_l3, res_l4, res_act


q_map = pd.read_csv('result3-2(300).csv', header=None)
q_map = pd.Series(q_map.iloc[:, 1].values.tolist(),
                  index=q_map.iloc[:, 0].values.tolist())
q_map = q_map.to_dict()


for _ in range(100):
    # ビンゴカード生成
    positions = [[[0 for i in range(5)] for j in range(5)] for k in range(4)]
    for i in range(4):
        line = [0 for i in range(5)]
        for n in range(5):
            line[n] = list(range(15*n+1, 15*n+16))
        for n in range(5):
            for m in range(5):
                positions[i][n][m] = random.choice(line[m])
                line[m].remove(positions[i][n][m])
        positions[i][2][2] = 0

    yet_numbers = list(range(1, 76))
    already_numbers = []
    stopflags = [0, 0, 0, 0]  # 0:継続、１：ストップ　２：アウト
    points = [0]

    while 0 in set(stopflags):

        l2 = [0, 0, 0, 0]
        l3 = [0, 0, 0, 0]
        l4 = [0, 0, 0, 0]
        for i in range(4):
            if stopflags[i] == 0:
                l2[i] = len(reach(positions[i], 2))
            if stopflags[i] == 0:
                l3[i] = len(reach(positions[i], 3))
            if stopflags[i] == 0:
                l4[i] = len(reach(positions[i], 4))
        s_a_ts = []
        for i in range(5):
            sorted_s = positions_sort(stopflags, l2, l3, l4, i)
            s_a_ts.append(board_to_str(sorted_s[0], sum(points),
                                       sorted_s[1], sorted_s[2], sorted_s[3], number_to_stopflag(sorted_s[4])))

        q_s_a_ts = []
        for i in s_a_ts:
            if i in q_map:
                q_s_a_ts.append(q_map[i])
            else:
                q_s_a_ts.append(0)

        act_stopflags = number_to_stopflag(q_s_a_ts.index(max(q_s_a_ts)))

        for i in range(4):
            if act_stopflags[i] == 1 and point(positions[i]) <= points[-1]:
                act_stopflags[i] = 0

            if act_stopflags[i] == 1 and stopflags[i] != 0:
                act_stopflags[i] = 0

        # ストップ
        for i in range(4):
            if stopflags[i] == 0 and act_stopflags[i] == 1:
                stopflags[i] = 1
                points.append(point(positions[i]))

        # ビンゴ回す
        number = random.choice(yet_numbers)
        already_numbers.append(number)

        # 穴開ける　ビンゴしたらその処理
        for i in range(4):
            if stopflags[i] == 0:
                open_bingo(number, positions[i])
                if bingo(positions[i]) == 1:
                    stopflags[i] = 2
                    points.append(0)

        yet_numbers.remove(number)

    print(points)
    # pprint.pprint(positions)
