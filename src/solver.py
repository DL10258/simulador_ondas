from functools import cache
import numpy as np 
#from scipy.sparse import diags
#from scipy.sparse.linalg import spsolve
import numba as nb 
datos_prueba={
    "hbar":1.0,
    "masa":1.0}
def normalizar(psi,dx):
    norma = np.sqrt(np.sum(np.abs(psi)**2) * dx)
    return psi / norma
def estado_inicial(x, dx, x0, sigma, k0):
    A = (1.0 / (2*np.pi*sigma**2))**0.25
    psi = A * np.exp(-((x - x0)**2) / (4*sigma**2)) * np.exp(1j*k0*x)
    return normalizar(psi,dx)
'''def operador_evolucion_temporal(N,largo_grilla,dt,datos_particula,V):
    dx=2*largo_grilla/N 
    alpha=datos_particula["hbar"]**2/(2*datos_particula["masa"]*dx**2)
    beta=1j*0.5*dt/datos_particula["hbar"]
    diag_principal=2*alpha+V 
    diag_secundaria=-alpha*np.ones(N-1)
    H=diags([diag_secundaria,diag_principal,diag_secundaria],[-1,0,1],format='csc')
    I=diags([np.ones(N)],[0],format='csc')
    A=I+beta*H
    B=I-beta*H 
    return A,B'''
'''def paso_tiempo(psi,A,B):
    rhs=B@ psi
    return spsolve(A,rhs)'''

def operador_evolucion_temporal(N,largo_grilla,dt,datos_particula,V):
    dx=2*largo_grilla/N 
    alpha=datos_particula["hbar"]**2/(2*datos_particula["masa"]*dx**2)
    beta=1j*0.5*dt/datos_particula["hbar"]
    diag_principal=2*alpha+V 
    diag_secundaria=-alpha*np.ones(N-1)
    a_principal=1+beta*diag_principal
    a_secundario=beta*diag_secundaria
    b_principal=1-beta*diag_principal
    b_secundario=-beta*diag_secundaria
    return [a_secundario,a_principal,a_secundario,b_secundario,b_principal,b_secundario]
@nb.njit(cache=True)
def thomas(a, b, c, d):
    n = len(d)
    c_ = np.empty(n, dtype=np.complex128)
    d_ = np.empty(n, dtype=np.complex128)
    x  = np.empty(n, dtype=np.complex128)
    c_[0] = c[0] / b[0]
    d_[0] = d[0] / b[0]
    for i in range(1, n):
        m     = b[i] - a[i-1] * c_[i-1]
        c_[i] = c[i] / m
        d_[i] = (d[i] - a[i-1] * d_[i-1]) / m
    x[-1] = d_[-1]
    for i in range(n-2, -1, -1):
        x[i] = d_[i] - c_[i] * x[i+1]
    return x
@nb.njit(cache=True)
def paso_tiempo(psi,a_sub,a_main,a_sup,b_sub,b_main,b_sup):
    n=len(psi)
    rhs=np.empty(n,dtype=np.complex128)
    rhs[0]=b_main[0]*psi[0]+b_sup[0]*psi[1]
    for i in range(1,n-1):
        rhs[i]=b_sub[i-1]*psi[i-1]+b_main[i]*psi[i]+b_sup[i]*psi[i+1]
    rhs[-1]=b_sub[-1]*psi[-2]+b_main[-1]*psi[-1]
    return thomas(a_sub,a_main,a_sup,rhs)
