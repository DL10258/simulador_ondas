from userprefs import *
from potenciales import *
from solver import *
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

datos = user_config()
datos.obtener_datos()
const_usuario = constantes_elegidas()
const_usuario.obtener_datosc()

dx = 2 * datos.params["grilla"] / int(datos.params["N"])
x = np.linspace(-datos.params["grilla"] + dx, datos.params["grilla"] - dx, int(datos.params["N"]))
psi_0 = estado_inicial(x, dx, **datos.params)

pot = c_potenciales()
mi_potencial = pot.muestrame()
V = pot.potencial[mi_potencial](x, **datos.params)
V = agregar_absorbente(V, x)
diags_AB = operador_evolucion_temporal(V, **datos.params, **const_usuario.constantes)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.labelsize": 14,
    "font.size": 12,
    "legend.fontsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
    "grid.color": "gray"
})

psi = psi_0.copy()
PASOS_POR_FRAME = 200
USAR_ABSORBENTE = True

N_puntos = int(datos.params["N"])
idx_sensor_izq = int(N_puntos * 0.15)
idx_sensor_der = int(N_puntos * 0.85)

T_acumulado = 0.0
R_acumulado = 0.0
dt = datos.params.get("dt", 0.01) 

fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(-datos.params["grilla"], datos.params["grilla"])
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$|\psi(x,t)|^2$")

V_visual = np.real(V).astype(np.float64)
V_abs_max = np.max(np.abs(V_visual))
if V_abs_max > 0:
    V_visual = (V_visual / V_abs_max) * 0.3

ax.set_ylim(float(V_visual.min()) - 0.05, 0.5)

ax.fill_between(x, V_visual, alpha=0.2, color='darkgoldenrod', label=r'$V(x)$')
ax.axhline(0, color='gray', lw=0.5, linestyle='-')

line, = ax.plot(x, np.abs(psi)**2, color='midnightblue', lw=1.5, label=r'$|\psi|^2$')

texto_T = ax.text(0.7, 0.9, r'$T = 0.000$', transform=ax.transAxes, fontsize=12,
                  bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))
texto_R = ax.text(0.1, 0.9, r'$R = 0.000$', transform=ax.transAxes, fontsize=12,
                  bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))

ax.axvline(x[idx_sensor_izq], color='red', linestyle=':', alpha=0.5, label='Sensor R')
ax.axvline(x[idx_sensor_der], color='green', linestyle=':', alpha=0.5, label='Sensor T')
ax.legend(loc='upper right', framealpha=0.9)

anim_running = True

def on_key(event):
    global anim_running
    if event.key == ' ':
        if anim_running:
            ani.pause()
            anim_running = False
            print("Simulación pausada.")
        else:
            ani.resume()
            anim_running = True
            print("Simulación reanudada.")
    elif event.key == 's':
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        pdf_name = f"snapshot_{timestamp}.pdf"
        png_name = f"snapshot_{timestamp}.png"
        fig.savefig(pdf_name, format='pdf', bbox_inches='tight')
        fig.savefig(png_name, format='png', dpi=300, bbox_inches='tight')
        print(f"Gráficas guardadas: {pdf_name} y {png_name}")

fig.canvas.mpl_connect('key_press_event', on_key)

def paquete_en_borde(psi_actual, dx_val, umbral=1e-3):
    borde_izq = np.sum(np.abs(psi_actual[:50])**2) * dx_val
    borde_der = np.sum(np.abs(psi_actual[-50:])**2) * dx_val
    return borde_izq > umbral or borde_der > umbral

def update(frame):
    global psi, T_acumulado, R_acumulado
    
    for _ in range(PASOS_POR_FRAME):
        psi = paso_tiempo(psi, *diags_AB)
        
        j_der = calcular_corriente(psi, idx_sensor_der, dx)
        j_izq = calcular_corriente(psi, idx_sensor_izq, dx)
        
        if j_der > 0:
            T_acumulado += j_der * dt
        if j_izq < 0:
            R_acumulado -= j_izq * dt
            
    if not USAR_ABSORBENTE and paquete_en_borde(psi, dx):
        psi = estado_inicial(x, dx, **datos.params)
        T_acumulado = 0.0
        R_acumulado = 0.0
        
    line.set_ydata(np.abs(psi)**2)
    texto_T.set_text(r'$T \approx {:.4f}$'.format(T_acumulado))
    texto_R.set_text(r'$R \approx {:.4f}$'.format(R_acumulado))
    
    return line, texto_T, texto_R

ani = animation.FuncAnimation(fig, update, frames=300, interval=20, blit=True)

plt.tight_layout()
print("Controles: [ESPACIO] para pausar/reanudar | [s] para guardar PDF y PNG")
plt.show()
