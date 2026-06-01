import numpy as np 
import numba as nb 
def corriente(psi,dx,idx,**kwargs):
    idx = np.clip(idx, 1, len(psi)-2)
    dpsi_dx=(psi[idx+1]-psi[idx-1])/(2*dx)
    dpsi_dx_c=(np.conj(psi[idx+1])-np.conj(psi[idx-1]))/(2*dx)
    J=1j*kwargs["hbar"]/(2*kwargs["masa"]) * (psi[idx]*dpsi_dx_c - np.conj(psi[idx])*dpsi_dx)
    return np.real(J)
def normalizar(psi,dx):
    norma = np.sqrt(np.sum(np.abs(psi)**2) * dx)
    return psi / norma
def estado_inicial(x, dx, **kwargs):
    A = (1.0 / (2*np.pi*kwargs["sigma"]**2))**0.25
    psi = A * np.exp(-((x - kwargs["x0"])**2) / (4*kwargs["sigma"]**2)) * np.exp(1j*kwargs["k0"]*x)
    return normalizar(psi,dx)
def operador_evolucion_temporal(V,**kwargs):
    dx=(kwargs["grillaD"]-kwargs["grillaI"])/kwargs["N"] 
    alpha=kwargs["hbar"]**2/(2*kwargs["masa"]*dx**2)
    beta=1j*0.5*kwargs["dt"]/kwargs["hbar"]
    diag_principal=2*alpha+V 
    diag_secundaria=-alpha*np.ones(kwargs["N"]-1)
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
        if i<n-1:
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
def incertidumbre(psi, x, dx, **kwargs):
    hbar = kwargs["hbar"]
    #masa = kwargs["masa"]
    densidad = np.abs(psi)**2
    x_med   = np.sum(x * densidad) * dx
    x2_med  = np.sum(x**2 * densidad) * dx
    delta_x = np.sqrt(np.abs(x2_med - x_med**2))
    dpsi    = np.gradient(psi, dx)
    d2psi   = np.gradient(dpsi, dx)
    p_med   = np.real(-1j * hbar * np.sum(np.conj(psi) * dpsi) * dx)
    p2_med  = np.real(-hbar**2 * np.sum(np.conj(psi) * d2psi) * dx)
    delta_p = np.sqrt(np.abs(p2_med - p_med**2))
    return delta_x, delta_p, delta_x * delta_p
def energia_total(psi,V,dx,**_):
    d2psi=np.gradient(np.gradient(psi,dx),dx)
    K=np.real(-0.5*(_["hbar"]/_["masa"])*np.sum(np.conj(psi)*d2psi)*dx)
    U=np.real(np.sum(np.abs(psi)**2*np.real(V))*dx)
    return K+U 
