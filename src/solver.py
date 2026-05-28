import numpy as np 
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
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
def operador_evolucion_temporal(N,largo_grilla,dt,datos_particula,V):
    dx=2*largo_grilla/N 
    alpha=datos_particula["hbar"]**2/(2*datos_particula["masa"]*dx**2)
    beta=1j*0.5*dt/datos_particula["hbar"]
    diag_principal=2*alpha+V 
    diag_secundaria=-alpha*np.ones(N-1)
    H=diags([diag_secundaria,diag_principal,diag_secundaria],[-1,0,1],format='csc')
    I=diags([np.ones(N)],[0],format='csc')
    A=I+beta*H
    B=I-beta*H 
    return A,B
def paso_tiempo(psi,A,B):
    rhs=B@ psi
    return spsolve(A,rhs)
