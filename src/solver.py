import numpy as np 
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def normalizar(psi):
    norma = np.sqrt(np.sum(np.abs(psi)**2) * dx)
    return psi / norma
def estado_inicial(x, x0=0.0, sigma=1.0, k0=5.0):
    A = (1.0 / (2*np.pi*sigma**2))**0.25
    psi = A * np.exp(-((x - x0)**2) / (4*sigma**2)) * np.exp(1j*k0*x)
    return normalizar(psi)

N=1500
a=30.0
dt=1e-4
dx=2*a/N 
x=np.linspace(-a+dx,a-dx,N)
hbar=1.0
m=1.0
alpha=hbar**2/(2*m*dx**2)
beta=1j*0.5*dt/hbar

V=np.zeros(N)
diag_principal=2*alpha+V
diag_secundaria=-alpha*np.ones(N-1)

H=diags([diag_secundaria,diag_principal,diag_secundaria],[-1,0,1],format='csc')
I=diags([np.ones(N)],[0],format='csc')

A=I+beta*H
B=I-beta*H 

def paso_tiempo(psi):
    rhs=B@ psi
    return spsolve(A,rhs)
