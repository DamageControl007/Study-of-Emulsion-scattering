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
import xlrd
import xlsxwriter
import sys
from datetime import date
from pysolar.solar import *
from datetime import datetime
import datetime
from solarpy import irradiance_on_plane
from datetime import datetime


START=datetime.now()
nm=10                                                                          #Number of hours in a day



def func1(var1):
    ps=[]
    for k in range (0, var1):
        ps.append(func2())
    func3(ps)

def func3(lst):
    for i in range(0, len(lst)):
        print(lst[i])

def func2():
    itr=int(1e6)                                                                 #number of iterations
    print(itr)

    # Monte carlo paramters
    Ut=0.2
    Us=Ut*1
    Ua=Ut-Us
    g=0.81

    # System boundaries
    Lx=1
    Ly=4.3
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

    # sensor coordinates

    sensor_z=14.6
    sensor_x=6
    sensor_y=0
    sensor_area=0.025


    for i in range(0,itr):
        if i%100000==0:
            print(i*100/itr,"%")
            
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
        
                                                                                    # if photon reaches the other boundary without any interaction
        if z>=Lz:
            path+=Lz
            thru+=1
            front+=1
            mass+=w
        
                                                                                    # if it reaches the inlet boundary
        elif z<=0:
            back+=1
            pass
        
                                                                                    # if it undergoes scattering
        else:
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
                    hit+=1
                    w=w*(1-Ua/Ut) 
                    path+=s
                    break
                elif z1>Lz:
                    d=abs((Lz-z)/Uz)
                    z1=Lz
                    x1=x+d*Ux
                    y1=y+d*Uy
                    path+=d
                    if abs(x1)>Lx/2 or abs(y1)>Ly/2:
                        sys=False
                        break
                    
                    # Checking total internal reflection at z=1
                    if N_re*np.sqrt(1-Uz**2)>1:
                        z=Lz
                        Uz=-Uz
                        s=s-d
                        x=x1
                        y=y1
                        
                    else:
                        mass+=w
                        front+=1
                        sys=False
                        break
                        

                else:
                    d=abs(z/Uz)
                    z=0
                    path+=d
                    x1=x+d*Ux
                    y1=y+d*Uy
                    if abs(x1)>Lx/2 or abs(y1)>Ly/2:
                        sys=False
                        mass+=w
                        break
                    
                    # checking internal reflection at z=0
                    if N_re*np.sin(np.arccos(Uz))>1:
                        z=0
                        x=x1
                        y=y1
                        s=s-d
                        Uz=-Uz
                    else:
                        z=z1
                        sys=False
                        back+=1
                        break

            #russian roulette
            if w<0.001:
                  m=10
                  e=random.uniform(0,1)
                  if e<=1/m:
                      w=w*m
                  else:
                      w=0        
    return path/itr


func1(nm)
  
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

        





        



