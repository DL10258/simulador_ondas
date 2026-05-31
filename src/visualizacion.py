import streamlit as st 
import scipy.constants as const 
import numpy as np 
import matplotlib.pyplot as plt 
from userprefs import *
import scienceplots
#import time 
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "font.size": 12,
    "axes.labelsize": 14,
    "legend.fontsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})
from solver import *
st.set_page_config(layout="wide",page_title="Simulador de ondas cuanticas")
def paquete_en_borde(psi_eval, dx_val, umbral=1e-3):
    borde_izq = np.sum(np.abs(psi_eval[:50])**2) * dx_val
    borde_der = np.sum(np.abs(psi_eval[-50:])**2) * dx_val
    return borde_izq > umbral or borde_der > umbral
if 'simulador_iniciado' not in st.session_state:
    st.session_state.user=user_config()
    st.session_state.constantes=constantes_elegidas()
    st.session_state.potenciales=c_potenciales()
    st.session_state.simulador_iniciado=True
st.title("Simulador de ondas en 1D")
st.sidebar.header("Panel de Control")
definir_entorno,definir_potencial,definir_particula,amortiguamiento=st.sidebar.tabs(["Entorno","Potencial","Partícula","Amortiguamiento"])
with definir_entorno:
    st.subheader("Unidades y Masa")
    sistema=st.radio("Unidades: ",["Atómicas","S.I."])
    if sistema == "Atómicas":
        st.session_state.constantes.constantes["hbar"]=1.0
        st.session_state.constantes.constantes["masa"]=st.number_input("Masa",value=1.0)
    else:
        st.session_state.constantes.constantes["masa"]=st.number_input("Masa (kg)", value=9.11e-31,format="%e")
        st.session_state.constantes.constantes["hbar"]=const.hbar
    st.write("---")
    st.subheader("Grilla Espacial")
    st.session_state.user.params["grillaI"]=st.number_input("Limites Izquierdo",value=0.0)
    st.session_state.user.params["grillaD"]=st.number_input("Limite Derecho",value=np.abs(st.session_state.user.params["grillaI"])+1.0,min_value=st.session_state.user.params["grillaI"]+1.0)
    st.session_state.user.params["N"]=st.number_input("Número de puntos",value=1500,min_value=1500,max_value=15000,step=500)
    st.session_state.user.params["dt"]=st.number_input(r"Paso temporal $(s)$",value=0.0001,format="%f")
with definir_potencial:
    st.subheader("Configura tu potencial")
    tipo_potencial=st.selectbox("Elegir",["Libre","Barrera","Pozo","Oscilador","Escalon"])
    if tipo_potencial=="Libre":
        pass
    elif tipo_potencial=="Escalon":
        st.session_state.user.params["V_0"]=st.number_input("Seleciona el valor del potencial",value=25.0,min_value=0.0,step=1.0)
        st.session_state.user.params["punto_potencial"]=st.number_input("Selecciona en donde comienza tu escalon",value=0.0)
    elif tipo_potencial=="Barrera":
        st.session_state.user.params["V_0"]=st.number_input("Seleccione el valor del potencial", value=st.session_state.user.params["V_0"],min_value=0.0,step=1.0)
        st.session_state.user.params["limite_izq"]=st.number_input("En donde inicia tu potencial",value=0.0,step=1.0)
        st.session_state.user.params["limite_der"]=st.number_input("En donde finaliza tu potencial",value=st.session_state.user.params["limite_izq"]+1.0,min_value=st.session_state.user.params["limite_izq"]+0.1,step=0.1)


    elif tipo_potencial=="Pozo":
        tipo_potencial=st.selectbox("Seleccione su pozo",["Pozo Finito","Pozo Infinito","Pozo Triangular","Doble Pozo"])
        if tipo_potencial=="Pozo Finito":
            st.session_state.user.params["V_0"]=st.number_input(r"Seleccione $V_0$",value=-25.0,max_value=0.0,step=1.0)
            st.session_state.user.params["limite_izq"]=st.number_input("En donde inicia tu pozo",value=0.0,step=1.0)
            st.session_state.user.params["limite_der"]=st.number_input("En donde finaliza tu pozo",value=st.session_state.user.params["limite_izq"]+1.0,min_value=st.session_state.user.params["limite_izq"]+0.1,step=0.1)
        elif tipo_potencial=="Pozo Infinito":
            st.session_state.user.params["V_0"]=1e10
            st.session_state.user.params["limite_izq"]=st.number_input("En donde se ubica tu primera barrera",value=0.0,step=1.0)
            st.session_state.user.params["limite_der"]=st.number_input("En donde se ubica tu barrera final",value=st.session_state.user.params["limite_izq"]+1.0,min_value=st.session_state.user.params["limite_izq"]+1.0,step=1.0)
        elif tipo_potencial=="Pozo Triangular":
            st.session_state.user.params["V_0"]=st.number_input(r"Seleccione $V_0$",value=-25.0,max_value=0.0,step=1.0)
            st.session_state.user.params["limite_izq"]=st.number_input("En donde inicia tu pozo",value=0.0,step=1.0)
            st.session_state.user.params["limite_der"]=st.number_input("En donde finaliza tu pozo",value=st.session_state.user.params["limite_izq"]+1.0,min_value=st.session_state.user.params["limite_izq"]+0.1,step=0.1)
        elif tipo_potencial=="Doble Pozo":
            st.session_state.user.params["lam"]=st.number_input(r"Introduzca la rigidez del potencial $(\lambda)$, valores comunes $(0,01 \to 0,05)$",value=0.001,step=0.001,format="%e")
            st.session_state.user.params["epsilon"]=st.number_input(r"Introduzca la asimetria de los pozos $\epsilon$",value=0.0,step=0.5)
            st.session_state.user.params["a"]=st.number_input(r"Separación entre pozos $(a)$",value=2.0,step=0.5)
    elif tipo_potencial=="Oscilador":
        tipo_potencial=st.selectbox("Seleccione su oscilador",["Oscilador Armonico"])
        if tipo_potencial=="Oscilador Armonico":
            st.session_state.user.params["omega"]=st.number_input(r"Seleccione $\omega$",value=1.0,step=1.0)
            st.session_state.user.params["centro"]=st.number_input("Elija el centro",value=0.0,step=1.0)
with definir_particula:
    st.subheader("Configura tu partícula")
    st.session_state.user.params["x0"]=st.number_input(r"Posición inicial $(x_0)$",min_value=st.session_state.user.params["grillaI"],max_value=st.session_state.user.params["grillaD"],value=(st.session_state.user.params["grillaI"]+st.session_state.user.params["grillaI"])/2.0,step=1.0)
    st.session_state.user.params["k0"]=st.number_input(r"Momento inicial $(k_0)$",value=0.0,step=1.0)
    st.session_state.user.params["sigma"]=st.number_input(r"Dispersión $(\sigma)$",value=1.0,min_value=0.1,step=1.0)
st.header("Visualización del Entorno")
with amortiguamiento:
    st.subheader("Configuración opcional para el amortiguamiento en bordes")
    st.session_state.user.params["ancho"]=st.number_input("Introduzca el ancho de amortiguamiento",value=3.0,min_value=1.0)
    st.session_state.user.params["fuerza"]=st.number_input("Introduzca la magnitud de la fuerza",value=15.0,min_value=1.0)

if st.button("INICIAR SIMULACIÓN", use_container_width=True):
    marco_grafica = st.empty()
    barra = st.progress(0)
    dx = (st.session_state.user.params["grillaD"] - 
          st.session_state.user.params["grillaI"]) / int(st.session_state.user.params["N"])
    x = np.linspace(st.session_state.user.params["grillaI"]+dx,
                    st.session_state.user.params["grillaD"]-dx,
                    int(st.session_state.user.params["N"]))
    potencial_elegido=tipo_potencial.lower().replace(" ","_")
    V = st.session_state.potenciales.selector(potencial_elegido)(x, **st.session_state.user.params)
    V = st.session_state.potenciales.absorbente(V, x,**st.session_state.user.params)
    diags_AB = operador_evolucion_temporal(V, **st.session_state.user.params,
                                            **st.session_state.constantes.constantes)
    psi = estado_inicial(x, dx, **st.session_state.user.params)
    a_sub, a_main, a_sup, b_sub, b_main, b_sup = diags_AB

    V_visual = np.real(V).astype(np.float64)
    V_abs_max = np.max(np.abs(V_visual))
    if V_abs_max > 0:
        V_visual = V_visual / V_abs_max * 0.3

    plt.style.use(['science', 'notebook', 'grid'])
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.minorticks_on()
    ax.grid(which='major', color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
    ax.grid(which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.1)
    ax.set_xlim(st.session_state.user.params["grillaI"],
                st.session_state.user.params["grillaD"])
    ax.set_ylim(min(-0.05, V_visual.min() - 0.05), 1.5)
    ax.set_xlabel(r"Posición $x$")
    ax.set_ylabel(r"Densidad $|\psi|^2$")
    ax.fill_between(x, V_visual, alpha=0.2, color='orange', label=r'$V(x)$')
    ax.axhline(0, color='gray', lw=0.5, linestyle='--')
    line, = ax.plot(x, np.abs(psi)**2, color='royalblue', lw=1.5, label=r"$|\psi|^2$")
    ax.legend(loc="upper right")

    PASOS_POR_FRAME = 500
    FRAMES_TOTALES = 2000 
    margen_pml = st.session_state.user.params["ancho"] + 2.0
    idx_R = np.argmin(np.abs(x - (st.session_state.user.params["grillaI"] + margen_pml)))
    idx_T = np.argmin(np.abs(x - (st.session_state.user.params["grillaD"] - margen_pml)))
    T_acum = 0.0
    R_acum = 0.0
    incidente_paso=False 
    for frame in range(FRAMES_TOTALES):
        J_T = corriente(psi,dx,idx_T,**st.session_state.user.params,**st.session_state.constantes.constantes)
        J_R = corriente(psi,dx,idx_R,**st.session_state.user.params,**st.session_state.constantes.constantes)
        norma = np.sum(np.abs(psi)**2) * dx
        for _ in range(PASOS_POR_FRAME):
            psi = paso_tiempo(psi, a_sub, a_main, a_sup, b_sub, b_main, b_sup)
        if J_R<0:
            incidente_paso=True
        T_acum += max(J_T,0)* st.session_state.user.params["dt"] * PASOS_POR_FRAME
        if incidente_paso:
            R_acum += max(-J_R,0) * st.session_state.user.params["dt"] * PASOS_POR_FRAME
        line.set_ydata(np.abs(psi)**2)
        ax.set_title(f"T ={T_acum:.3f}      R={R_acum:.3f}      T+R={T_acum+R_acum:.3f}       Norma={norma:.3f}")
        marco_grafica.pyplot(fig)
        barra.progress((frame + 1) / FRAMES_TOTALES)
    plt.close(fig)  # libera memoria
    st.success("¡Simulación finalizada!")  
