from random import*
condition=[[0 for i in range(5)] for j in range(5)]
line=[0]*5
for n in range(5):
    line[n]=list(range(15*n+1,15*n+16))
for n in range(5):
    for m in range(5):
        condition[n][m]=choice(line[m])
        line[m].remove(condition[n][m])
print(condition)
        
