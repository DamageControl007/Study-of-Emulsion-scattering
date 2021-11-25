# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:21:14 2021


@author: Somendra Singh Jadon
"""
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import miepython as mp
import csv
import xlrd
import xlsxwriter
import sys
from datetime import date
from pysolar.solar import *
import datetime
from solarpy import irradiance_on_plane

nm=10                                                                          #Number of hours in a day
itr=100000                                                                   #number of iterations


# Monte carlo paramters
Ut=1
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
beta=858


IntensityLoss=0.05         # Fraction of intensity loss while exiting the system by a photon

# Observation 
photon=0
path=0
front=0
back=0
thru=0
mass=0
hit=0
absorbed_path=0

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
    w=1       # photon weight
    
    e=random.uniform(0,1)
    
    # initializing coordinates
    x=0
    y=0
    z=0
    e=random.uniform(0,1)
    s=-np.log(e)/Ut          # Photon step size
    x=s*Ux
    y=s*Uy
    z=s*Uz
    sys=True
    lim=0
    
    # if photon reaches the other boundary without any interaction
    if z>Lz:
        path+=Lz
        thru+=1
        front+=1
        mass+=w
        w=w*math.exp(-beta*Lz)
        absorbed_path+=Lz*w
    
    # if it reaches the inlet boundary
    elif z<0:
        back+=1
        pass
    
    # if it undergoes scattering
    else:
        hit+=1
        w=w*math.exp(-beta*s)
        absorbed_path+=w*s
        
    # While a photon is inside the system boundaries
    while 0<=z<=Lz and sys and w>0.0005:
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
        decoy=True
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
                w=w*math.exp(-beta*s)
                absorbed_path+=w*s
                path+=s
                break
            elif z1>Lz:
                d=abs((Lz-z)/Uz)
                z1=Lz
                x1=x+d*Ux
                y1=y+d*Uy
                path+=d
                w=w*math.exp(-beta*d)
                absorbed_path+=w*d
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
                    x=x1
                    y=y1
                    z=z1
                    sin=(N_re/M_re)*np.sqrt(1-Uz**2)
                    Uy=Uy*(N_re/M_re)
                    Ux=Ux*(N_re/M_re)
                    norm=np.sqrt(Ux**2+Uy**2+Uz**2)
                    Ux=Ux/norm
                    Uy=Uy/norm
                    Uz=Uz/norm
                    # system has a thickness of 0.1 cm
                    d1=abs(0.1/Uz)
                    x=x + d1*Ux
                    y=y + d1*Uy
                    sin=M_re*sin
                    Uz=np.sqrt(1-sin**2)
                    Uy=(M_re)*Uy
                    Ux=(M_re)*Ux
                    norm=np.sqrt(Ux**2+Uy**2+Uz**2)
                    Ux=Ux/norm
                    Uy=Uy/norm
                    Uz=Uz/norm
                    d2=abs((sensor_z-z)/Uz)
                    x=x + d2*Ux
                    y=y + d2*Uy
                    radius=(x-sensor_x)**2+(y-sensor_y)**2
                    if radius<=sensor_area/3.14:
                        photon+=(1-IntensityLoss)
                        print('photon= ', photon)
                    break
                    

            else:
                d=abs(z/Uz)
                z=0
                path+=d
                x1=x+d*Ux
                y1=y+d*Uy
                w=w*math.exp(-beta*d)
                absorbed_path+=w*d
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
  
print("I/Io at the detector=", photon/itr)   
print("Thru=", thru/itr)
print("hits=", hit/itr)
print("absorbed_path= ", absorbed_path/itr);


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

        





        



