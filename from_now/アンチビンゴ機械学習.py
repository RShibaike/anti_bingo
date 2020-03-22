from random import*


#穴を開ける関数
#x:番号, y:ビンゴの局面
def open(x,y):
    for n in range(5):
        if x in y[n]:
            y[n][y[n].index(x)]=0


#nマス連続で空いている箇所が何箇所ある判定する関数
#x:ビンゴの局面, y:nマス, return:そこあけるとビンゴになる数のリスト
def reach(x,y):
    #counter変数初期化
    counter=[]
    #横列
    for n in x:
        if n.count(0)==y:
            counter+=n
    #line変数初期化
    line=[0 for i in range(5)]
    #縦列
    for n in range(5):
        for m in range(5):
            line[m]=x[m][n]
        if line.count(0)==y:
            counter+=line
    #右斜め列
    for n in range(5):
        line[n]=x[n][n]
    if line.count(0)==y:
        counter+=line
    #左斜め列
    for n in range(5):
        line[n]=x[4-n][n]
    if line.count(0)==y:
        counter+=line
    #0削除
    while 0 in counter:counter.remove(0)

    return counter


#ビンゴしてるかどうか調べてくれる関数
#x:ビンゴの局面, return:ビンゴしてたら１、してないと０
def bingo(x):
    #counter変数初期化
    counter=0
    #横列
    for n in x:
        if n.count(0)==5:
            counter=1
    #line変数初期化
    line=[0 for i in range(5)]
    #縦列
    for n in range(5):
        for m in range(5):
            line[m]=x[m][n]
        if line.count(0)==5:
            counter=1
    #右斜め列
    for n in range(5):
        line[n]=x[n][n]
    if line.count(0)==5:
        counter=1
    #左斜め列
    for n in range(5):
        line[n]=x[4-n][n]
    if line.count(0)==5:
        counter=1

    return counter


#現在の得点を測る（空いてるマス数を数える）関数
#ビンゴしてたらちゃんとゼロになる
#x:ビンゴの局面, return:得点
def point(x):
    counter=0
    if bingo(x)==1:
        return 0
    else:
        numbers_of_bingo=[]
        for n in x:numbers_of_bingo+=n
        while 0 in numbers_of_bingo:
            numbers_of_bingo.remove(0)
            counter+=1
        return counter


#期待値だしてくれる関数
#x:ビンゴの局面, y:まだ出てない数字, return:期待値
def expected_value(x,y):
    return (25-point(x))/len(y)-len(reach(x,4))/len(y)*point(x)


#ビンゴを書き出してくれる関数
#x:ビンゴの局面
def output(x):
    op=[[0 for i in range(5)] for j in range(5)]
    for i in range(5):
        for j in range(5):
            op[i][j]=str(x[i][j])
            if(0<=int(op[i][j])<=9):
                op[i][j]="0"+op[i][j]
        a=str(op[i])
        a=a.replace(",","")
        a=a.replace("'","")
        a=a.strip("[")
        a=a.strip("]")
        print(a)

"""
↑関数
''''''''''''''''''''''''''''''''''''''''''''''''
↓本文
"""
#カウンター初期化
total=0
out=0


for i in range(100):
    #ビンゴカード生成
    position=[[0 for i in range(5)] for j in range(5)]
    line=[0]*5
    for n in range(5):
        line[n]=list(range(15*n+1,15*n+16))
    for n in range(5):
        for m in range(5):
            position[n][m]=choice(line[m])
            line[m].remove(position[n][m])
    position[2][2]=0

    #ビンゴ書き出し
    output(position)

    print("-------------------------")

    #初期化
    yet_numbers=list(range(1,76))
    already_numbers=[]
    stopflag=0

    #ストップorアウトまで続ける
    while stopflag==0 and bingo(position)==0:
        if expected_value(position,yet_numbers)<=0:
            stopflag=1
        number=choice(yet_numbers)
        already_numbers.append(number)
        open(number,position)
        yet_numbers.remove(number)


    #ビンゴ書き出し
    output(position)

    total+=point(position)
    if bingo(position)==1:out+=1
    print(point(position))
    print("=========================")

print("total:"+ str(total))
print("アウト回数:"+str(out))
print("平均:"+str(total/100))
print("アウト除いた平均:"+str(total/(100-out)))








