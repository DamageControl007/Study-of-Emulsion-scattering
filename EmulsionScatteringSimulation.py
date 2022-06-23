#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 17:53:39 2022

@author: somendrasinghjadon
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import miepython as mp
import csv
import xlsxwriter
import sys
from datetime import date
from pysolar.solar import *
from datetime import datetime
import datetime
from solarpy import irradiance_on_plane
from datetime import datetime
import threading


START=datetime.now()
nm=10                                                                          #Number of hours in a day
ps=[]


aaaa=1

def func1(var1, Ut_K, Ua_K, g):
    global ps, file_path
    Ut=Ut_K
    Ua=Ut*Ua_K
    for i in range(var1):
        file_path.write(str(g)+"\t")
        file_path.write(str(Ut)+"\t")
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
    global filepath, bta                                                                        
    #Optimization of iterations 
    if (Ut<1e-4):
        itr=int(1e7)
    elif (Ut<1e-3):
        itr=int(1e6)
    elif (Ut<1):
        itr=int(1e6)
    elif (Ut<11):
        itr=int(1e6)
    else:
        itr=int(1e5)  
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
    prev=0
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
    for i in range(0,itr):
        #if i%100000==0:
            #print(i*100/itr,"%")      
                                                                                    # Initializing direction cosines    
        Ux=0
        Uy=0
        Uz=1
        w=1                                                                         # photon weight
                                                                                 # initializing coordinates
        x=0
        y=0
        z=0
        x_list=[]
        y_list=[]
        z_list=[]
        e=random.uniform(0,1)
        s=-np.log(e)/Ut                                                             # Photon step size
        x=s*Ux
        y=s*Uy
        z=s*Uz
        sys=True
        lim=0
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
        
                                                                                    # if it reaches the inlet boundary
        elif z<=0:
            back+=1
            pass
        
                                                                                    # if it undergoes scattering
        else:
            path+=s
            hit+=1
            
                                                                                    # While a photon is inside the system boundaries
        while 0<z<Lz and sys and w>0.0005:
            e=random.uniform(0,1)
            phi=e*2*3.14
    # =============================================================================
    #           e=random.uniform(0,1)
    #             for k in range(0,interval):
    #                 if zz[n][k]>e:
    #                     theta=(k*(180/interval)*(np.pi/180))
    #                     break
    # =============================================================================
            e=random.uniform(0,1)
            if (abs(g)<0.001):
                theta = np.pi*random.uniform(0,1)
            else:
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
                    x_list.append(x)
                    y_list.append(y)
                    z_list.append(z)
                    hit+=1
                    #w=w*(1-Ua/Ut) 
                    w=w*np.exp(-bta*s)
                    path+=s
                    norm_path+=s*w
                    largest_s=Find_Max(largest_s, z)
                    break
                elif z1>Lz:
                    d=abs((Lz-z)/Uz)
                    w=w*np.exp(-bta*d)
                    z1=Lz
                    x1=x+d*Ux
                    y1=y+d*Uy
                    x_list.append(x1)
                    y_list.append(y1)
                    z_list.append(z1)
                    path+=d
                    norm_path+=d*w
                    largest_s=Find_Max(largest_s, z1)
                    if abs(x1)>Lx/2 or abs(y1)>Ly/2:
                        
                        sys=False
                        max_z_avg+=largest_s
                        break
                    
                    # Checking total internal reflection at z=1
                    if N_re*np.sqrt(1-Uz**2)<0:   #Not including TIR
                        
                        z=Lz
                        Uz=-Uz
                        s=s-d
                        x=x1
                        y=y1
                        TIR+=1
                        
                    else:
                        mass+=w
                        front+=1
                        sys=False
                        max_z_avg+=largest_s
                        break
                        

                else:
                    d=abs(z/Uz)
                    w=w*np.exp(-bta*d)
                    z=0
                    path+=d
                    norm_path+=d*w
                    largest_s=Find_Max(largest_s, z)
                    
                    x1=x+d*Ux
                    y1=y+d*Uy
                    x_list.append(x1)
                    y_list.append(y1)
                    z_list.append(z)
                    if abs(x1)>Lx/2 or abs(y1)>Ly/2:
                        
                        sys=False
                        mass+=w
                        max_z_avg+=largest_s
                        break
                    
                    # checking internal reflection at z=0
                    if N_re*np.sin(np.arccos(Uz))<0:   #Not including TIR
                        
                        z=0
                        x=x1
                        y=y1
                        s=s-d
                        Uz=-Uz
                        TIR+=1
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
    file_path.write(str(path/itr)+"\t")
    file_path.write(str(norm_path/itr)+"\t")
    file_path.write(str(hit/itr)+"\t")
    file_path.write(str(back/itr)+"\t")
    file_path.write(str(front/itr)+"\t")
    file_path.write(str(thru/itr)+"\t")
    file_path.write(str(mass/itr)+"\t")
    file_path.write(str(absorbed/itr) +"\t")
    file_path.write(str(TIR/itr)+"\t")
    file_path.write(str(max_z_avg/itr) + "\t")
    
    file_path.write(str("{:e}".format(itr))+"\n")
    return path/itr



if __name__ == "__main__":
# =============================================================================
#     t1=threading.Thread(target=func1, args=(0.1, 0,0.9))
#     t2=threading.Thread(target=func1, args=(0.1, 0, 0.9))
#     t3=threading.Thread(target=func1, args=(0.1, 0, 0.9))
#     t1.start()
#     t2.start()
#     t3.start()
#     
#     t1.join()
#     t2.join()
#     t3.join()
# =============================================================================]
    Ut=1
    absorption=0.1
    g=0.9
    bta=0
    text="FinalData_g"+str(int(g*10))+"_Ua:_"+str(bta)+".txt"

    print(text)
    file_path = open(text,"a")
    file_path.write("Anisotropy" +"\t")
    file_path.write("Interaction coefficient"+"\t")
    file_path.write("L/L0"+"\t")
    file_path.write("Weight norm L/L0" +"\t")
    file_path.write("Collisions"+"\t")
    file_path.write("Backscattered"+"\t")
    file_path.write("Front"+"\t")
    file_path.write("Undeflected" +"\t")
    file_path.write("Mass"+"\t")
    file_path.write("Photons absorbed"+"\t")
    file_path.write("TIR"+"\t")
    file_path.write("Avg max z coordinate"+"\t")
    file_path.write("Iterations"+"\n")
    for i in range(0,1):
        func1(50,Ut,absorption,g)
        print(i)
        Ut=Ut*10
    
    #func3(ps)
    file_path.close()
    
    print("done")

  
# =============================================================================
# print("L/L0", path/itr)   
# print("Thru=", thru/itr)
# print("hits=", hit/itr)
# =============================================================================


print("Execution time: ", (datetime.now()-START))

# =============================================================================
# with open(heading + '_'+ wavelength + ' nm'+".csv", 'w', newline='') as f:
#     thewriter=csv.writer(f)
#     thewriter.writerow(['Normalised weigth L/Lo vs volume fraction'])
#     thewriter.writerow(['wavelength'])
#     thewriter.writerow([ wavelength])
#     thewriter.writerow(['Time', 'I/Io', 'backscattering','pm2.5','PBLH', 'UtxLo'])
#     for i in range(0,nm):
#         thewriter.writerow([time[i], weight[i], knight[i], pm[i], boun[i], UtxLo[i]])
# =============================================================================

        





        



