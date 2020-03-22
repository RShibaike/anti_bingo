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


#穴を開ける関数
#x:番号, y:ビンゴの局面
def open_bingo(x, y):
    for n in range(5):
        if x in y[n]:
            y[n][y[n].index(x)] = 0


#nマス連続で空いている箇所が何箇所ある判定する関数
#x:ビンゴの局面, y:nマス, return:そこあけるとビンゴになる数のリスト
def reach(x, y):
    #counter変数初期化
    counter = []
    #横列
    for n in x:
        if n.count(0) == y:
            counter += n
    #line変数初期化
    line = [0 for i in range(5)]
    #縦列
    for n in range(5):
        for m in range(5):
            line[m] = x[m][n]
        if line.count(0) == y:
            counter += line
    #右斜め列
    for n in range(5):
        line[n] = x[n][n]
    if line.count(0) == y:
        counter += line
    #左斜め列
    for n in range(5):
        line[n] = x[4-n][n]
    if line.count(0) == y:
        counter += line
    #0削除
    while 0 in counter:
        counter.remove(0)

    return counter


#ビンゴしてるかどうか調べてくれる関数
#x:ビンゴの局面, return:ビンゴしてたら１、してないと０
def bingo(x):
    #counter変数初期化
    counter = 0
    #横列
    for n in x:
        if n.count(0) == 5:
            counter = 1
    #line変数初期化
    line = [0 for i in range(5)]
    #縦列
    for n in range(5):
        for m in range(5):
            line[m] = x[m][n]
        if line.count(0) == 5:
            counter = 1
    #右斜め列
    for n in range(5):
        line[n] = x[n][n]
    if line.count(0) == 5:
        counter = 1
    #左斜め列
    for n in range(5):
        line[n] = x[4-n][n]
    if line.count(0) == 5:
        counter = 1

    return counter


#現在の得点を測る（空いてるマス数を数える）関数
#ビンゴしてたらちゃんとゼロになる
#x:ビンゴの局面, return:得点
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


#期待値だしてくれる関数
#x:ビンゴの局面, y:まだ出てない数字, return:期待値
def expected_value(x, y):
    return (25-point(x))/len(y)-len(reach(x, 4))/len(y)*point(x)


#ビンゴを書き出してくれる関数
#x:ビンゴの局面
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


#positions(ビンゴカードの盤面), stopflags（ストップされてるかどうかのフラグ）,
#points（前のポイントを取得するのに使う）, position_value（空いてる箇所による点数）,
#position_point（穴の数、２、３、４連続の箇所の数にかける係数）, how_stop（前の点数に対していつとめるか）
#return 次のあるべきstop_flags
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

        elif stopflags[i] == 0 and point(positions[i]) > 4 and  value[i] > how_stop[points[-1] - 5 + counter]:
            return_stopflags[i] = 1
            counter += 1

    return return_stopflags







position_values = [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 
                    [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]
position_points = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
how_stops = [[50, 60, 70, 80, 90, 100, 110,
            120, 130, 140, 150, 160, 170, 180, 190],
            [50, 60, 70, 80, 90, 100, 110,
             120, 130, 140, 150, 160, 170, 180, 190],
            [50, 60, 70, 80, 90, 100, 110,
             120, 130, 140, 150, 160, 170, 180, 190],
            [50, 60, 70, 80, 90, 100, 110,
             120, 130, 140, 150, 160, 170, 180, 190],
            [50, 60, 70, 80, 90, 100, 110,
             120, 130, 140, 150, 160, 170, 180, 190],
            [50, 60, 70, 80, 90, 100, 110,
             120, 130, 140, 150, 160, 170, 180, 190]]

for i in range(14):
        position_values.append([0, 0, 0, 0, 0])
        position_points.append([0, 0, 0, 0])
        how_stops.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])




for c in range(400):

        strength = [0 for i in range(20)]

        random_list_position_values = [[0 for i in range(6)] for i in range(5)]
        for i in range(5):
            for j in range(6):
                random_list_position_values[i][j] = position_values[j][i]

        random_list_position_points = [[0 for i in range(6)] for i in range(4)]
        for i in range(4):
            for j in range(6):
                random_list_position_points[i][j] = position_points[j][i]

        random_list_how_stops = [[0 for i in range(6)] for i in range(15)]
        for i in range(15):
            for j in range(6):
                random_list_how_stops[i][j] = how_stops[j][i]




        for i in range(14):
            average = 0
            for j in range(5):
                mean = statistics.mean(random_list_position_values[j])
                pstdev = statistics.pstdev(random_list_position_values[j])
                position_values[i + 6][j] = random.uniform(mean-2*pstdev, mean+2*pstdev)
                average += (position_values[i+6][j]**2)
            average = math.sqrt(average)
            for j in range(5):
                position_values[i+6][j] = round(position_values[i+6][j]/average, 4)
        
        for i in range(14):
            average = 0
            for j in range(4):
                mean = statistics.mean(random_list_position_points[j])
                pstdev = statistics.pstdev(random_list_position_points[j])
                position_points[i + 6][j] = random.uniform(mean-2*pstdev, mean+2*pstdev)
                average += (position_points[i+6][j]**2)
            average = math.sqrt(average)
            for j in range(4):
                position_points[i+6][j] = round(position_points[i+6][j]/average, 4)

        for i in range(14):
            average = 0
            for j in range(15):
                mean = statistics.mean(random_list_how_stops[j])
                pstdev = statistics.pstdev(random_list_how_stops[j])
                how_stops[i + 6][j] = random.uniform(mean-2*pstdev, mean+2*pstdev)
                average += (how_stops[i+6][j]**2)
            average = math.sqrt(average)
            for j in range(15):
                how_stops[i+6][j] = round(how_stops[i+6][j]/average, 4)
        
        







        # for i in range(14):
        #     position_values[i+6][0] = 1
        #     for j in range(4):
        #         mean = statistics.mean(random_list_position_values[j])
        #         pstdev = statistics.pstdev(random_list_position_values[j])
        #         position_values[i+6][j+1] = random.uniform(mean-2*pstdev, mean+2*pstdev)
        #         position_values[i+6][j+1] = round(position_values[i+6][j+1], 2)

        # for i in range(14):
        #     position_points[i+6][0] = 1
        #     for j in range(3):
        #         mean = statistics.mean(random_list_position_points[j])
        #         pstdev = statistics.pstdev(random_list_position_points[j])
        #         position_points[i+6][j+1] = random.uniform(mean-2*pstdev, mean+2*pstdev)
        #         position_points[i+6][j+1] = round(position_points[i+6][j+1], 2)

        # for i in range(14):
        #     how_stops[i+6][0] = 1
        #     for j in range(20):
        #         mean = statistics.mean(random_list_how_stops[j])
        #         pstdev = statistics.pstdev(random_list_how_stops[j])
        #         how_stops[i+6][j+1] = random.uniform(mean-2*pstdev, mean+2*pstdev)
        #         how_stops[i+6][j+1] = round(how_stops[i+6][j+1], 2)

        with open('C:\\Users\\Shibaike Ryoya\\Desktop\\anti_bingo\\genetic_algorithm\\result3.txt', 'a', encoding='utf-8') as f:
            for j in range(5):
                mean = statistics.mean(random_list_position_values[j])
                pstdev = statistics.pstdev(random_list_position_values[j])
                f.write("position_value" + "平均:" + str(mean) +
                        " 標準偏差:" + str(pstdev) + "\n")
            for j in range(4):
                mean = statistics.mean(random_list_position_points[j])
                pstdev = statistics.pstdev(random_list_position_points[j])
                f.write("position_points" + "平均:" + str(mean) +
                        " 標準偏差:" + str(pstdev) + "\n")
            for j in range(15):
                mean = statistics.mean(random_list_how_stops[j])
                pstdev = statistics.pstdev(random_list_how_stops[j])
                f.write("how_stop" + "平均:" + str(mean) +
                        " 標準偏差:" + str(pstdev) + "\n")

        if c == 0:
            for i in range(20):
                for j in range(5):
                    position_values[i][j] = random.uniform(0, 100)
                    position_values[i][j] = round(position_values[i][j], 2)
            for i in range(20):
                for j in range(4):
                    position_points[i][j] = random.uniform(0, 100)
                    position_points[i][j] = round(position_points[i][j], 2)
            for i in range(20):
                for j in range(15):
                    how_stops[i][j] = random.uniform(0, 100)
                    how_stops[i][j] = round(how_stops[i][j], 2)

        
        remain_time = 0
        for a in range(20):
            for l in range(100):
                #ビンゴカード生成
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

                #ビンゴ書き出し
                # output(positions)

                # print("-------------------------")

                #初期化
                yet_numbers = list(range(1, 76))
                already_numbers = []
                stopflags = [0,0,0,0]
                points = [0]

                #ストップorアウトまで続ける
                while stopflags != [1,1,1,1]:
                    number = random.choice(yet_numbers)
                    already_numbers.append(number)

                    stopflags2 = evaluation_function(positions, stopflags, 
                                            points, position_values[a], position_points[a], how_stops[a])
                    
                    # print(stopflags2)

                    for i in range(4):
                    
                        if stopflags[i] == 0 and stopflags2[i] == 1 and point(positions[i]) > points[-1]:
                            stopflags[i] = 1
                            points.append(point(positions[i]))

                        else:
                            open_bingo(number, positions[i])
                            if stopflags[i] == 0 and bingo(positions[i]) == 1:
                                stopflags[i] = 1
                                points.append(0)
            
                    yet_numbers.remove(number)

                for m in range(5):
                    strength[a] += points[m] 



            remain_time += 1
            # sys.stdout.write("\r%d /400" % remain_time)
            # sys.stdout.flush()

        return_list = []

        for i in range(20):
            co = []
            co.append(position_values[i])
            co.append(position_points[i])
            co.append(how_stops[i])
            co.append(strength[i])
            return_list.append(co)

        # print(return_list)

        return_list.sort(key=lambda x: x[3], reverse=True)

        # with open('result.txt', mode='w') as f:
        #     f.write(str(return_list))

        # file = open('result.txt', 'w')
        # file.write("a")
        # file.close()

        with open('C:\\Users\\Shibaike Ryoya\\Desktop\\anti_bingo\\genetic_algorithm\\result3.txt', 'a', encoding='utf-8') as f:
            for i in range(6):
                f.write(str(return_list[i]) + "\n")

        for i in range(6):
            position_values[i] = return_list[i][0]
            position_points[i] = return_list[i][1]
            how_stops[i] = return_list[i][2]

        sys.stdout.write("\r%d /400" % c)
        sys.stdout.flush()
