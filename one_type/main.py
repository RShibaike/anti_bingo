import os
import shutil
import random
import sys
import numpy as np
import tensorflow as tf
from collections import deque
from bingo import Bingo
from dqn import Policy
from dqn import Memory


def output(x):
    op = [[0 for i in range(5)] for j in range(5)]
    for i in range(5):
        for j in range(5):
            op[i][j] = str(x[i][j])
            if(0 <= int(op[i][j]) <= 9):
                op[i][j] = "0"+op[i][j]
        a = str(op[i])
        a = a.replace(",", "")
        a = a.replace("'", "")
        a = a.strip("[")
        a = a.strip("]")
        print(a)


def converter(card, turn):
    res = np.array(card)
    res = res.flatten()
    res = np.append(res, turn)

    return res


bingo = Bingo()
policy = Policy()
memory = Memory()


for c in range(10000):

    bingo.bingo_card = bingo.make_bingo()
    bingo.game_flag = True  # gameが進行中ならTrue
    bingo.bingo_card = bingo.make_bingo()
    bingo.yet_numbers = list(range(1, 76))  # 抽選されていない数のリスト
    bingo.point = 0

    while bingo.game_flag:
        state = policy.converter(bingo.bingo_card, len(bingo.yet_numbers))
        action = policy.choose_action(state)
        if action == 1:
            bingo.stop()
            memory.store(state, 1, bingo.point, state)

        else:
            bingo.do_move()
            next_state = policy.converter(
                bingo.bingo_card, len(bingo.yet_numbers))
            memory.store(state, 0, 0, next_state)

        if memory.t_memory >= 99:
            # print(memory.sample())
            policy.learn_act(memory.sample()[0], memory.sample()[1],
                             memory.sample()[2], memory.sample()[3])
        sys.stdout.write("\r%d /10000" % memory.t_memory)

    sys.stdout.write("\r%d /10000" % c)

# policy.summary()
# policy.save()

bingo.game_flag = True
bingo.bingo_card = bingo.make_bingo()
while bingo.game_flag:
    state = policy.converter(bingo.bingo_card, len(bingo.yet_numbers))
    action = policy.choose_action(state)
    if action == 1:
        bingo.stop()
        # memory.store(state, 1, bingo.point, state)

    else:
        bingo.do_move()
        next_state = policy.converter(bingo.bingo_card, len(bingo.yet_numbers))
        # memory.store(state, 0, 0, next_state)

    output(bingo.bingo_card)
