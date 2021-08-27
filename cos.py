import random

g=0.1
x=0
itr=1000000
for i in range(0,itr):
    e=random.uniform(0,1)
    cos=(1/(2*g))*(1 + g**2 - ((1-g**2)/(1+g*(2*e - 1)))**2)
    x+=cos
file_path = open("cos.txt","a")
file_path.write(str(g)+"\t")
file_path.write(str(x/itr)+"\n")
file_path.close()