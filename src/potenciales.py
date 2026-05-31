import numpy as np 
def agregar_absorbente(V, x, **kwargs):
    V_abs = V.astype(complex)
    x_min, x_max = x[0], x[-1]
    mask_izq = x < (x_min + kwargs["ancho"])
    mask_der = x > (x_max - kwargs["ancho"])
    V_abs[mask_izq] -= 1j * kwargs["fuerza"] * ((x_min + kwargs["ancho"] - x[mask_izq]) / kwargs["ancho"])**2
    V_abs[mask_der] -= 1j * kwargs["fuerza"] * ((x[mask_der] - (x_max - kwargs["ancho"])) / kwargs["ancho"])**2
    return V_abs
def libre(x,**kwargs):
    V=np.zeros_like(x)
    return V
def pozo_infinito(x,**kwargs):
    V=np.full_like(x,kwargs["valor_infinito"],dtype=np.float64)
    V[(x>=kwargs["limite_izq"])&(x<=kwargs["limite_der"])]=0.0
    return V 
def escalon(x,**kwargs):
    V=np.zeros_like(x)
    V[x>=kwargs["punto_potencial"]]=kwargs["V_0"]
    return V 
def barrera(x,**kwargs):
    V=np.zeros_like(x)
    V[(x>=kwargs["limite_izq"])&(x<=kwargs["limite_der"])]=kwargs["V_0"]
    return V
def pozo_finito(x,**kwargs):
    V=np.zeros_like(x)
    V[(x>=kwargs["limite_izq"])&(x<=["limite_der"])]=-np.abs(kwargs["V_0"])
    return V 
def pozo_triangular(x,**kwargs):
    V = np.zeros_like(x, dtype=np.float64)
    xc = (kwargs["limite_izq"] + kwargs["limite_der"]) / 2      
    a  = (kwargs["limite_der"] - kwargs["limite_izq"]) / 2      
    mask = (x >= kwargs["limite_izq"]) & (x <= kwargs["limite_der"])
    V[mask] = -np.abs(kwargs["V_0"]) * (1 - np.abs(x[mask] - xc) / a)
    return V
def oscilador_armonico(x,**kwargs):
    return 0.5 * kwargs["omega"]**2 * (x-kwargs["centro"])**2
def doble_pozo(x,**kwargs):
    return kwargs["lam"] * (x**2 - kwargs["a"]**2)**2 + kwargs["epsilon"] * x 
