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
V=pot.potencial[mi_potencial](x,**datos.datos_potencial())
V=agregar_absorbente(V,x)
diags_AB=operador_evolucion_temporal(*datos.datos_operador_temporal(),const_usuario.constantes,V)


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
V_visual = np.real(V).astype(np.float64)
V_abs_max = np.max(np.abs(V_visual))
if V_abs_max > 0:
    V_visual = V_visual / V_abs_max * 0.3
else:
    V_visual = V_visual

ax.set_ylim(float(V_visual.min()) - 0.05, 0.5)
ax.fill_between(x, V_visual, alpha=0.2, color='orange', label='V(x)')
ax.axhline(0, color='gray', lw=0.5, linestyle='--')
line, = ax.plot(x, np.abs(psi)**2, color='royalblue', lw=1.5)

'''def update(frame):
    global psi
    for _ in range(PASOS_POR_FRAME):
        psi = paso_tiempo(psi, A, B)
    line.set_ydata(np.abs(psi)**2)
    return line,'''
USAR_ABSORBENTE = True  # cambia según el potencial
def paquete_en_borde(psi, dx, umbral=1e-3):
    borde_izq = np.sum(np.abs(psi[:50])**2) * dx
    borde_der = np.sum(np.abs(psi[-50:])**2) * dx
    return borde_izq > umbral or borde_der > umbral
def update(frame):
    global psi
    for _ in range(PASOS_POR_FRAME):
        psi = paso_tiempo(psi, *diags_AB)
    if not USAR_ABSORBENTE and paquete_en_borde(psi, dx):
        psi = estado_inicial(x, dx, datos.params["x0"], datos.params["sigma"], datos.params["k0"])
    line.set_ydata(np.abs(psi)**2)
    return line,
ani = animation.FuncAnimation(fig, update, frames=300, interval=20, blit=True)
plt.tight_layout()
plt.show()

