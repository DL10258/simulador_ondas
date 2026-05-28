from userprefs import *
from potenciales import *
from solver import *
import numpy as np 

datos=user_config()
datos.obtener_datos()
const_usuario=constantes_elegidas()
const_usuario.obtener_datosc()
dx=2*datos.params["grilla"]/int(datos.params["N"])
x=np.linspace(-datos.params["grilla"]+dx,datos.params["grilla"]-dx,int(datos.params["N"]))
psi_0=estado_inicial(x,dx,datos.params["x0"],datos.params["sigma"],datos.params["k0"])
pot=c_potenciales()
mi_potencial=pot.muestrame()
V=pot.potencial[mi_potencial](x,*datos.datos_potencial())
A,B=operador_evolucion_temporal(*datos.datos_operador_temporal(),const_usuario.constantes,V)


#De aqui para abajo fue robado pero igual no sirve, si encuentras una mejor manera de ejecutar esto, seria lo mejor.
import matplotlib.pyplot as plt
import matplotlib.animation as animation

psi = psi_0.copy()
PASOS_POR_FRAME = 200

fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(-datos.params["grilla"], datos.params["grilla"])
ax.set_ylim(0, 0.5)
ax.set_xlabel("x")
ax.set_ylabel(r"$|\psi|^2$")

# potencial escalado visualmente
V_max = V.max() if V.max() > 0 else 1.0
ax.fill_between(x, V/V_max * 0.4, alpha=0.15, color='orange', label='V(x)')
line, = ax.plot(x, np.abs(psi)**2, color='royalblue', lw=1.5)

def update(frame):
    global psi
    for _ in range(PASOS_POR_FRAME):
        psi = paso_tiempo(psi, A, B)
    line.set_ydata(np.abs(psi)**2)
    return line,

ani = animation.FuncAnimation(fig, update, frames=300, interval=20, blit=True)
plt.tight_layout()
plt.show()

