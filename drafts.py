a=1
c=1
num = 0
for j in range (132):
    for i in range (132):
        if 2*(a+j)>c+i and a+j+c+i>a+j:
            if 2*a+c+i==130:
                num += 1
print(num)