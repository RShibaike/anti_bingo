#初期化
condition=[[0 for i in range(5)] for j in range(5)]
yet_numbers=list(range(1,76))

#ファイルからの読み込み
with open('bingo.txt','r') as f:
    n=0
    for line in f:
        x=line.split()
        if n<=4:
            for m in range(5):
                condition[n][m]=int(x[m])
        if n==5:
            for m in x:
                yet_numbers.remove(int(m))
        n+=1
        
    
for i in condition:print(i)
#print(yet_numbers)


#nマス連続で空いている箇所の残りのマスを返す関数
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
def expected_value(x,y):
    
    return (25-point(x))/len(y)-len(reach(x,4))/len(y)*point(x)
    
    
#本文
print(point(condition))
#print(point(condition))        
    
        
    


