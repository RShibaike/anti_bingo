from bingo import Bingo
from dqn import Policy
from dqn import Memory
import numpy as np
import tensorflow as tf


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


bingo = Bingo()
policy = Policy()
memory = Memory()

policy.load()

bingo.bingo_card = bingo.make_bingo()

while bingo.game_flag:
    state = policy.converter(bingo.bingo_card, len(bingo.yet_numbers))
    action = policy.choose_action(state)
    if action == 1:
        bingo.stop()
        memory.store(state, 1, bingo.point, state)

    else:
        bingo.do_move()
        next_state = policy.converter(bingo.bingo_card, len(bingo.yet_numbers))
        memory.store(state, 0, 0, next_state)

    output(bingo.bingo_card)
