# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 09:47:36 2020

@author: GRUPO 3 - MCOC2020

Felipe Bravo
Jose Tomás Martinez
Eduardo Torres
"""
from matplotlib.pylab import *
from matplotlib.pyplot import imshow
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

#Geometria
a = 1.         #[m] alto del dominio
b = 1.         #[m] ancho del dominio
Nx = 30       # intervalos en x
Ny = 30       # intervalos en y

dx = b/Nx
dy = a/Ny

h = dx

if dx != dy:
    print("ERROR! dy != dy")
    exit(-1)      #-1, le dice al SO que el programa falló

#funcion de cenveniencia para calcular las coordenadas del punto (i,j)
def coords(i,j):
    return(dx*i,dy*j)
x,y = coords(4,2)

print(f"x = {x}")
print(f"y = {y}")

def imshowbien(u):
    imshow(u.T[Nx::-1,:],cmap=cm.coolwarm,interpolation='bilinear')
    cbar = colorbar(extend = 'both', cmap= cm.coolwarm)
    ticks = np.arange(0,35,5)
    ticks_Text = ["{}°".format(deg) for deg in ticks]
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(ticks_Text)
    clim(0,30)
    
    xlabel('b')
    ylabel('a')
    xTicks_N= np.arange(0,Nx+1,3)
    yTicks_N= np.arange(0,Ny+1,3)
    xTicks= [coords(i,0)[0] for i in xTicks_N]
    yTicks= [coords(0,i)[1] for i in yTicks_N]
    xTicks_Text = ["{0:.2f}".format(tick) for tick in xTicks]
    yTicks_Text = ["{0:.2f}".format(tick) for tick in yTicks]
    xticks(xTicks_N,xTicks_Text, rotation='vertical')
    yticks(yTicks_N,yTicks_Text)
    margins(0.2)
    subplots_adjust(bottom=0.15)
    
u_k = np.zeros((Nx+1, Ny+1), dtype = np.double) #dtype es el tipo de dato
u_km1 = np.zeros((Nx+1, Ny+1),dtype = np.double) #dtype es el tipo de dato

#condicion de borde inicial
u_k[:,:] = 20              #20 grados inicial en todas partes

#parametros problema Hierro
dt = 0.01
K = 79.5                   # m^2/s
c = 450.                   # J/kg C
ρ = 7800.                  # kg/m^3
α = K*dt/(c*ρ*dx**2)

#informar cosas interesantes
print(f"dt = {dt}")
print(f"K = {K}")
print(f"c = {c}")
print(f"ρ = {ρ}")
print(f"α = {α}")

#loop en el tiempo
minuto = 60. #[s]
hora = 3600. #[s]
dia = 24 * hora

dt = 1 * minuto
dnext_t = 0.5 * hora      #guardar imagen cada 30 min

next_t = 0
framenum = 0

T = 1*dia
Days= 1 *T                # cuantos dias quiero simular

# Vectores para acumular la temperatura en puntos interesantes
u_0 = np.zeros(np.int32(Days/dt))
u_N4 = np.zeros(np.int32(Days/dt))
u_2N4 = np.zeros(np.int32(Days/dt))
u_3N4 = np.zeros(np.int32(Days/dt))
u_0c = np.zeros(np.int32(Days/dt))
u_N4c = np.zeros(np.int32(Days/dt))
u_2N4c = np.zeros(np.int32(Days/dt))
u_3N4c = np.zeros(np.int32(Days/dt))

def truncate(n,decimales=0):
    multiplier= 10**decimales
    return int(n*multiplier)/multiplier

#Loop de tiempo
for k in range(np.int32(Days/dt)):
    t = dt*(k+1)
    dias = truncate(t/dia, 0)
    horas = truncate((t-dias*dia)/hora, 0)
    minutos = truncate((t-dias*dia-horas*hora)/minuto, 0)
    titulo = "k = {0:05.0f} ".format(
        k) + " t = {0:02.0f}d {1:02.0f}h {2:02.0f}m".format(dias, horas, minutos)
    print(titulo)
    
   
    #CB esenciales, se repite en cada iteracion
    u_k[0 , :] = 20.                          #Borde izquierdo
    #u_k[-1 ,:] = 0.                           #borde derecho
    u_k[: ,-1] = 0                    #borde superior
    u_k[: , 0] = 20                            #borde inferior


    #u_k[0,:] = u_k[-2,:]-0*dx                  #Borde izquierdo gradiente
    u_k[-1,:] = u_k[-2,:]-0*dx                 #Borde derecho gradiente
    #u_k[:,-1] = u_k[:,-2]-0*dy            #borde gradiente superior
    #u_k[:,0] = u_k[:,-2]-0*dy                  #Borde inferior gradiente
    
    #Loop en el espacio i = 1 ..... n-1
    for i in range(1,Nx):
        for j in range(1,Ny):
            #algoritmo de diferencias finitas 2-D para difusion
            
            #Lapaceano
            nabla_u_k = (u_k[i-1, j]+u_k[i+1,j]+u_k[i,j-1]+u_k[i,j+1]-4*u_k[i,j])/h**2
            
            #forward Euler
            u_km1[i,j] = u_k[i,j]+α*nabla_u_k
            
    #avanzar la solucion a k+1
    u_k = u_km1
    
    
    #CB esenciales, se repite en cada iteracion
    u_k[0 , :] = 20.                          #Borde izquierdo
    #u_k[-1 ,:] = 0.                           #borde derecho
    u_k[: ,-1] = 0                    #borde superior
    u_k[: , 0] = 20                            #borde inferior


    #u_k[0,:] = u_k[-2,:]-0*dx                  #Borde izquierdo gradiente
    u_k[-1,:] = u_k[-2,:]-10*dx                 #Borde derecho gradiente
    #u_k[:,-1] = u_k[:,-2]-0*dy            #borde gradiente superior
    #u_k[:,0] = u_k[:,-2]-0*dy                  #Borde inferior gradiente
    
    
    #Encuentro la temperatura en puntos interesantes
    u_0[k] = u_k[int(Nx/2),-1]                    #Superficie
    u_N4[k] = u_k[int(Nx/2),int(Ny/4)]            #N/4, medio
    u_2N4[k] = u_k[int(Nx/2),int(2*Ny/4)]         #2N/4, medio
    u_3N4[k] = u_k[int(Nx/2),int(3*Ny/4)]         #3N/4, medio

        #Encuentro la temperatura en puntos interesantes

    u_N4c[k]  = u_k[int(Nx/2),int(Ny/2)]             #N/4, medio
    u_2N4c[k] = u_k[int(Nx/2),int(3*Ny/4)]           #2N/4, medio
    u_3N4c[k] = u_k[int(3*Nx/4),int(3*Ny/4)]           #3N/4, medio
    
    #grafico en d_next
    if t> next_t:
        plt.figure(1)
        imshowbien(u_k)
        plt.title(titulo)
        plt.savefig("fig/caso_2_{0:04.0f}.png".format(framenum))
        framenum+=1
        next_t+= dnext_t
        plt.close(1)

#plotear histria de temperatura en puntos interesantes
plt.figure(2)

plt.plot(range(np.int32(Days/dt)),u_N4, label="N/4")
plt.plot(range(np.int32(Days/dt)),u_2N4, label="2N/4")
plt.plot(range(np.int32(Days/dt)),u_3N4, label="3N/4")
plt.plot(range(np.int32(Days/dt)),u_0, label="superficie")
plt.title("Evolucion de temperatura en puntos en caso 2")
plt.legend()
plt.savefig("EvolucionT_caso_2.png")


#plotear histria de temperatura en puntos pedidos
plt.figure(3)
plt.plot(range(np.int32(Days/dt)),u_N4c, label="a/2 , b/2")
plt.plot(range(np.int32(Days/dt)),u_2N4c, label="a/2 , 3b/4")
plt.plot(range(np.int32(Days/dt)),u_3N4c, label="3a/4 , 3b/4")
plt.title("Evolucion de temperatura en puntos en caso 2 puntos")
plt.legend()
plt.savefig("EvolucionT_caso_2_puntos.png")
plt.show()

