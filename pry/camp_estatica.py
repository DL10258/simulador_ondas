import numpy as np 
import matplotlib.pyplot as plt 

L=50.0
N=10000 
x=np.linspace(0,L,N)

x0=30.0
sigma=5.0
k0=2.0

A = (1.0 / (np.pi * sigma**2))**0.25
psi_0=A*np.exp(1j*k0*x)*np.exp(-(1/2*sigma**2)*(x-x0)**2)

prob_0=np.abs(psi_0)**2 

plt.figure(figsize=(8, 4))
plt.plot(x, prob_0, color='blue', lw=2, label=r'$|\psi(x,0)|^2$ (Probabilidad)')
plt.fill_between(x, prob_0, color='blue', alpha=0.2)

plt.title("Estado Inicial: Paquete de Ondas Gaussiano en t=0")
plt.xlabel("Posición (x)")
plt.ylabel("Densidad de Probabilidad")
plt.xlim(29, 31)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.show()
