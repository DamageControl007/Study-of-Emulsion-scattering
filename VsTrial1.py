import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


list1=[1,2,3]
list2=[4,5,6]
list3=[7,8,9]
data=[[0,0,0]]
for i in range(0, len(list1)):
    data[0].append(list1[i])
    data[0].append(list2[i])
    data[0].append(list3[i])
data.append([0,0,0])
for i in range(0, 2):
    data[1].append(list1[i])
    data[1].append(list2[i])
    data[1].append(list3[i])
data[1].append(-1)
print(data)
# data2=[]
# data2.append(list1)
# data2.append(list2)
# data2.append()
# data2.append([list1[0], list2[0], list3[0]])
# print(data2)
df=pd.DataFrame(data)
print(df)
file_name = 'MarksData2.xlsx'
  
# saving the excel
df.to_excel(file_name)
df = pd.read_excel (r'MarksData.xlsx')
pika=df.to_numpy()
print(pika[0,1][4])
origin=(0,0,0)
cor=(1,2,3)
yor=(5,4,6)
list5=[[]]
# list5.append(origin)
# list5[0].append(yor)
# list5.append(origin)
# list5[1].append(cor)

dff=pd.DataFrame(list5)
file_name='D2list.xlsx'
dff.to_excel(file_name)
df_nm=df.to_numpy()
#print(df_nm[0,1][1])
#print (df.loc[0].iat[1].iat[0])

print("Hello cosmos")
print("great to see you here")