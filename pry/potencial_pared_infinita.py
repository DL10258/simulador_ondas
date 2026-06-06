import numpy as np 
import matplotlib.pyplot as plt 

L=60.0
N=2000 
x=np.linspace(-L,0,N)

x0=-30.0 
a=5.0
k0=2.0
m=1.0
h=1.0
A=(2*a**2 /np.pi)**0.25


def psi(x,t):
    theta = 0.5 * np.arctan(2 *h* t / (m * a**2))
    phi = -theta - (h * k0**2 / (2*m)) * t
    y=A*(np.exp(1j*phi)/(a**4 + (4* h**2 * t**2)/m**2)**0.25)*np.exp(1j*k0*x)*np.exp(-(x-x0-(h*k0/m)*t)**2/(a**2 + (2j*h*t)/(m)))
    return y

from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(10, 5))

linea_prob, = ax.plot(x, np.abs(psi(x, 0)-psi(-x,0))**2, color='blue', lw=2, label=r'$|\psi(x,t)|^2$')

ax.set_xlim(-L, 30)
ax.set_ylim(0, 0.50)
ax.axvline(x=0,color='red',linestyle='--')
ax.set_title("Evolución Analítica del Paquete de Ondas bajo un potencial escalon infinito")
ax.set_xlabel("Posición (x)")
ax.set_ylabel("Densidad de Probabilidad")
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

dt = 0.25

def actualizar(frame):
    t_actual = frame * dt
    y_nueva = psi(x, t_actual)-psi(-x,t_actual) 
    linea_prob.set_ydata(np.abs(y_nueva)**2)
    return linea_prob,

animacion = FuncAnimation(fig, actualizar, frames=165, interval=30, blit=True)
plt.show()

