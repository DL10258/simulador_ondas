import numpy as np 
def agregar_absorbente(V, x, ancho=3.0, fuerza=15.0):
    V_abs = V.astype(complex)
    x_min, x_max = x[0], x[-1]
    mask_izq = x < (x_min + ancho)
    mask_der = x > (x_max - ancho)
    V_abs[mask_izq] -= 1j * fuerza * ((x_min + ancho - x[mask_izq]) / ancho)**2
    V_abs[mask_der] -= 1j * fuerza * ((x[mask_der] - (x_max - ancho)) / ancho)**2
    return V_abs
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
def pozo_triangular(x, limite_izq, limite_der, V_0, **kwargs):
    V = np.zeros_like(x, dtype=np.float64)
    xc = (limite_izq + limite_der) / 2      
    a  = (limite_der - limite_izq) / 2      
    mask = (x >= limite_izq) & (x <= limite_der)
    V[mask] = -np.abs(V_0) * (1 - np.abs(x[mask] - xc) / a)
    return V
def oscilador_armonico(x, omega=1.0, **kwargs):
    return 0.5 * omega**2 * x**2
def doble_pozo(x, lam=0.1, a=3.0, epsilon=0.3, **kwargs):
    return lam * (x**2 - a**2)**2 + epsilon * x 
