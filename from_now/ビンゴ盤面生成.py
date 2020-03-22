from random import*

#穴を開ける関数
def open(x,y):
    for n in range(5):
        if x in y[n]:
            y[n][y[n].index(x)]=0

#ビンゴカード生成
condition=[[0 for i in range(5)] for j in range(5)]
line=[0]*5
for n in range(5):
    line[n]=list(range(15*n+1,15*n+16))
for n in range(5):
    for m in range(5):
        condition[n][m]=choice(line[m])
        line[m].remove(condition[n][m])
condition[2][2]=0
for i in condition:print(i)

#入力手数進める
turn=int(input("数字を入力してください"))     
numbers=[]
numbers2=list(range(1,76))

for n in range(turn):
    res=choice(numbers2)
    numbers.append(res)
    open(res,condition)
    numbers2.remove(res)
for i in condition:print(i)
print(numbers)
