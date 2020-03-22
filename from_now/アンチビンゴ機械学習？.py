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


#ビンゴを書き出す関数
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


#５×５の空リストをいれるとビンゴカードにしてくれる関数
def make_bingo(x):
    line=[0]*5
    for n in range(5):
        line[n]=list(range(15*n+1,15*n+16))
    for n in range(5):
        for m in range(5):
            x[n][m]=choice(line[m])
            line[m].remove(x[n][m])
    x[2][2]=0
    


#ビンゴカードと思考回路いれると自己対戦してくれる関数
#x:ビンゴカード, y:思考回路
def self_play(x,y):
    #初期化
    yet_numbers=list(range(1,76))
    already_numbers=[]
    stopflag=0

    #ストップorアウトまで続ける
    while stopflag==0 and bingo(x)==0:
        if y(x,yet_numbers)<=0.09:
            stopflag=1
        number=choice(yet_numbers)
        already_numbers.append(number)
        open(number,x)
        yet_numbers.remove(number)



"""
↑関数
''''''''''''''''''''''''''''''''''''''''''''''''
↓本文
"""
#累計データ初期化
key=""
total_data=[]
out_data=[]
average_data=[]
average_excepted_out_data=[]
while key!="e":
    #カウンター初期化
    total=0
    out=0
    average=0
    average_excepted_out=0
    loop=10000

    #100回スタート
    for i in range(loop):
        
        #ビンゴカード生成
        position=[[0 for i in range(5)] for j in range(5)]
        make_bingo(position)
        #ビンゴ書き出し
        #output(position)
        #print("-------------------------")
        #自己対戦
        self_play(position,expected_value)
        #ビンゴ書き出し
        #output(position)
        #集計
        total+=point(position)
        if bingo(position)==1:out+=1
        #得点表示
        #print(point(position))
        #print("=========================")

    #結果発表
    average=total/loop
    average_excepted_out=round(total/(loop-out),3)
    total_data.append(total)
    out_data.append(out)
    average_data.append(average)
    average_excepted_out_data.append(average_excepted_out)

    print("total:"+ str(total))
    print("アウト回数:"+str(out))
    print("平均:"+str(average))
    print("アウト除いた平均:"+str(average_excepted_out))
    print("累計")
    print("total:"+ str(total_data))
    print("アウト回数:"+str(out_data))
    print("平均:"+str(average_data))
    print("アウト除いた平均:"+str(average_excepted_out_data))
    key=input("Eキーで終了します")

input("エンターキーで終了します")






