from random import*
import copy


#穴を開ける関数
#x:番号, y:ビンゴの局面
def open(x, y):
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
        if stopflags[i] == 0 and value[i] > how_stop[points[-1] + counter]:

            return_stopflags[i] = 1
            counter += 1

    return return_stopflags


"""
↑関数
''''''''''''''''''''''''''''''''''''''''''''''''
↓本文
"""
#カウンター初期化
total = 0
out = 0

position_value = [1, 31.21, 4.92, 12.27, 8.98]
position_point = [1, -8.99, -4.33, 73.79]
how_stop = [1, 75.28, 74.14, 4.95, 94.35, 7.16, 81.99, 104.37, 84.37, 65.19, 57.34, 3.23, -68.94, 44.92, 46.73, 196.64, 66.1, 13.24, 44.68, 41.5, -33.91]


    #ビンゴカード生成
positions = [[[0 for i in range(5)] for j in range(5)] for k in range(4)]
for i in range(4):
    line = [0 for i in range(5)]
    for n in range(5):
        line[n] = list(range(15*n+1, 15*n+16))
    for n in range(5):
        for m in range(5):
            positions[i][n][m] = choice(line[m])
            line[m].remove(positions[i][n][m])
    positions[i][2][2] = 0

#ビンゴ書き出し

    # print("-------------------------")

    #初期化
yet_numbers = list(range(1, 76))
already_numbers = []
stopflags = [0, 0, 0, 0]
points = [0]

    #ストップorアウトまで続ける
    # while stopflags != [1, 1, 1, 1]:
for i in range(75):
    number = choice(yet_numbers)
    already_numbers.append(number)
    stopflags2 = evaluation_function(positions, stopflags,
                                         points, position_value, position_point, how_stop)


    for i in range(4):
        if stopflags[i] == 0 and stopflags2[i] == 1 and point(positions[i]) > points[-1]:
            stopflags[i] = 1
            points.append(point(positions[i]))

        else:
            open(number, positions[i])
            if stopflags[i] == 0 and bingo(positions[i]) == 1:
                stopflags[i] = 1
                points.append(0)


    output(positions)
    input()
    print(stopflags2)
    print(stopflags)
    print(points)
    print(number)

print("最終結果：" + str(points))
    


    # total += point(position)
    # if bingo(position) == 1:
    #     out += 1
    # print(point(position))
    # print("=========================")


# print("total:" + str(total))
# print("アウト回数:"+str(out))
# print("平均:"+str(total/100))
# print("アウト除いた平均:"+str(total/(100-out)))
