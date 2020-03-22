from random import*

numbers=list(range(1,76))

while len(numbers)>=1:
    res=choice(numbers)
    print(res)
    numbers.remove(res)
    input("エンターキーを押してください")
print("終了です")
