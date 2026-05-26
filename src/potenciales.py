import numpy as np 

def pozo_infinito(x,limite_izq,limite_der,valor_infinito=1e10):
    V=np.full_like(x,valor_infinito,dtype=np.float64)
    V[(x>=limite_izq)&(x<=limite_der)]=0.0
    return V 
def escalon(x,punto_potencial,V_0):
    V=np.zeros_like(x)
    V[(x>=punto_potencial)]=V_0 
    return V
def barrera(x,limite_izq,limite_der,V_0):
    V=np.zeros_like(x)
    V[(x>=limite_izq)&(x<=limite_der)]=V_0
    return V
def pozo_finito(x,limite_izq,limite_der,V_0):
    V=np.zeros_like(x)
    V[(x>=limite_izq)&(x<=limite_der)]=-np.abs(V_0)
    return V 
