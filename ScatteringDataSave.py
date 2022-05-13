#Date: 11 May 2022
#Author: Somendra Singh Jadon
#Location: Central Library, Indian Institute of Technology, Delhi
#Local time: 2:20 PM
#python3

import numpy as np
import pandas as pd
import openpyxl
import sys
import csv
from datetime import date
from datetime import datetime
import threading
import random

print("Actual start")


START=datetime.now()
nm=10
ps=[]
aaaa=1

def func1(var1, Ut_K, Ua_K, g):
    global ps, file_path
    Ut=Ut_K
    Ua=Ut*Ua_K
    for i in range(var1):
        ps.append(func2(Ut, Ua, g))
        Ut+=Ut_K
        Ua=Ut*Ua_K
    
def Find_Max(a, b):
    if (a<b):
        return b
    return a

def func3(lst):
    for i in range(0, len(lst)):
        print(lst[i])

def func2(Ut, Ua, g):                                                                       
    #Optimization of iterations 
    if (Ut<1e-4):
        itr=int(1e3)
    elif (Ut<1e-3):
        itr=int(1e1)
    elif (Ut<1):
        itr=int(1e6)
    elif (Ut<10):
        itr=int(1e6)
    else:
        itr=int(1e3)  
    global aaaa
    print(aaaa)
    aaaa+=1
    # Monte carlo paramters
    Us=Ut-Ua
    # System boundaries
    Lx=1E3
    Ly=1E3
    Lz=1
    # refractive index of particles and medium (water)
    M_re=1.5837
    N_re=1.33
    IntensityLoss=0.05         # Fraction of intensity loss while exiting the system by a photon
    # Observation 
    photon=0
    path=0
    front=0
    back=0
    thru=0
    mass=0
    hit=0
    largest_s=0
    max_z_avg=0
    absorbed=0
    norm_path=0
    TIR=0
    DataFile=[[0,0,0]]
    n_hits=[]

    for i in range(0,itr):
        if (i>0.1):
            DataFile.append([0,0,0])
        # Initializing direction cosines    
        Ux=0
        Uy=0
        Uz=1
        w=1                                                                         # photon weight
        # initializing coordinates
        x=0
        y=0
        z=0
        e=random.uniform(0,1)
        s=-np.log(e)/Ut                                                             # Photon step size
        x=s*Ux
        y=s*Uy
        z=s*Uz
        sys=True
        lim=0
        x_cor=[]
        y_cor=[]
        z_cor=[]
        largest_s=0
        #largest_s=Find_Max(largest_s, s)
                                                                                    # if photon reaches the other boundary without any interaction
        if z>=Lz:
            path+=Lz
            norm_path+=Lz*w
            thru+=1
            front+=1
            mass+=w
            max_z_avg+=Lz
            x_cor.append(0)
            y_cor.append(0)
            z_cor.append(Lz)
            
        
                                                                                    # if it reaches the inlet boundary
        elif z<=0:
            back+=1
            x_cor.append(0)
            y_cor.append(0)
            z_cor.append(0)
            
            pass
        
        # if it undergoes scattering
        else:
            hit+=1
            x_cor.append(0)
            y_cor.append(0)
            z_cor.append(z)
            
        # While a photon is inside the system boundaries
        hit_count=0
        while 0<z<Lz and sys and w>0.0005 and hit_count<=100:
            
            e=random.uniform(0,1)
            phi=e*2*3.14
            e=random.uniform(0,1)
            cos=(1/(2*g))*(1 + g**2 - ((1-g**2)/(1+g*(2*e - 1)))**2)
            theta=np.arccos(cos)
            sin_theta=np.sin(theta)
            cos_theta=np.cos(theta)
            sin_phi=np.sin(phi)
            cos_phi=np.cos(phi)
            #Updating direction cosines
            if abs(Uz)>0.99999:
                Uz_1=np.sign(Uz)*cos_theta
                Uy_1=sin_theta*cos_phi
                Ux_1=sin_theta*sin_phi
            else:
                Usqr=np.sqrt(1-Uz**2)
                Uz_1=-sin_theta*cos_phi*Usqr + Uz*cos_theta
                Ux_1=(sin_theta*(Uz*Ux*cos_phi - Uy*sin_phi)/(Usqr)) + Ux*cos_theta
                Uy_1=(sin_theta*(Uz*Uy*cos_phi + Ux*sin_phi)/(Usqr)) + Uy*cos_theta
            Ux=Ux_1
            Uz=Uz_1
            Uy=Uy_1
            e=random.uniform(0,1)
            s=-np.log(e)/Ut
            loop=True
            while loop:
                z1=z+s*Uz
                x1=x+s*Ux
                y1=y+s*Uy
                if 0<=z1<=Lz:
                    x=x1
                    y=y1
                    z=z1
                    x_cor.append(x)
                    y_cor.append(y)
                    z_cor.append(z)
                    hit+=1
                    hit_count+=1
                    w=w*(1-Ua/Ut) 
                    path+=s
                    norm_path+=s*w
                    largest_s=Find_Max(largest_s, z)
                    loop=False
                    break
                elif z1>Lz:
                    d=abs((Lz-z)/Uz)
                    z1=Lz
                    x1=x+d*Ux
                    y1=y+d*Uy
                    path+=d
                    norm_path+=d*w
                    largest_s=Find_Max(largest_s, z1)
                    x_cor.append(x1)
                    y_cor.append(y1)
                    z_cor.append(Lz)
                    if abs(x1)>Lx/2 or abs(y1)>Ly/2:
                        sys=False
                        max_z_avg+=largest_s
                        break
                        
                    else:
                        mass+=w
                        front+=1
                        sys=False
                        max_z_avg+=largest_s
                        break
                else:
                    d=abs(z/Uz)
                    z=0
                    path+=d
                    norm_path+=d*w
                    largest_s=Find_Max(largest_s, z)
                    
                    x1=x+d*Ux
                    y1=y+d*Uy
                    x_cor.append(x1)
                    y_cor.append(y1)
                    z_cor.append(0)
                    if abs(x1)>Lx/2 or abs(y1)>Ly/2:
                        sys=False
                        mass+=w
                        max_z_avg+=largest_s
                        break
                    
                    else:
                        z=z1
                        sys=False
                        back+=1
                        max_z_avg+=largest_s
                        break

            #russian roulette
            if w<0.001:
                  m=10
                  e=random.uniform(0,1)
                  if e<=1/m:
                      w=w*m
                  else:
                      absorbed+=1
                      w=0  
        n_hits.append(len(x_cor))
        for data in range(0,len(x_cor)):
            DataFile[i].append(z_cor[data])
            DataFile[i].append(x_cor[data])
            DataFile[i].append(y_cor[data])
        DataFile[i].append(-1)
    nf=pd.DataFrame(n_hits)
    print(nf)
    ExcelData=pd.DataFrame(DataFile)
    ExcelData.insert(0, 'Hits', nf)
    #ExcelData = pd.concat([pd.Series(nf, index=ExcelData.index, name='Collisions'), ExcelData], axis=1)
    print(ExcelData)
    return ExcelData



if __name__ == "__main__":
    Ut=1
    absorption=0
    g=0.7
    text="DataFile_g0"+str(int(g*10))+"_Ut"+str(int(Ut))+".csv"
    print(text)
    for i in range(0,1):
        (func1(1,Ut,absorption,g))
        print(i)
        Ut=Ut*10
    
    #func3(ps)
    print(ps[0])
    ps[0].to_csv(text)
    print("done")



print("Execution time: ", (datetime.now()-START))


        





        



