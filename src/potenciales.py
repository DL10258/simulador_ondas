import numpy as np 
def libre(x,**kwargs):
    V=np.zeros_like(x)
    return V
def pozo_infinito(x,limite_izq,limite_der,valor_infinito=1e10,**kwargs):
    V=np.full_like(x,valor_infinito,dtype=np.float64)
    V[(x>=limite_izq)&(x<=limite_der)]=0.0
    return V 
def escalon(x,limite_izq,limite_der,V_0,punto_potencial,**kwargs):
    if limite_izq<=limite_der:
        V=np.zeros_like(x)
        V[(x>=punto_potencial)]=V_0 
        return V
    else:
        return np.zeros_like(x)
def barrera(x,limite_izq,limite_der,V_0,**kwargs):
    V=np.zeros_like(x)
    V[(x>=limite_izq)&(x<=limite_der)]=V_0
    return V
def pozo_finito(x,limite_izq,limite_der,V_0,**kwargs):
    V=np.zeros_like(x)
    V[(x>=limite_izq)&(x<=limite_der)]=-np.abs(V_0)
    return V 
