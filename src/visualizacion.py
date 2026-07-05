import scipy.constants as const
from userprefs import *
from solver import *
from potenciales import *

import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# Umbrales para el indicador de normalización
_NORM_OK    = 0.01   # |‖ψ‖² - 1| < 1 %  → verde
_NORM_WARN  = 0.05   # |‖ψ‖² - 1| < 5 %  → amarillo
# cualquier cosa mayor                     → rojo


class GraficadoraEfectoTunel:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Efecto Túnel Cuántico")
        self.root.geometry("1200x720")

        # --- CONTENEDORES PRINCIPALES ---
        self.frame_controles = ttk.Frame(self.root, padding=15, width=440)
        self.frame_controles.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.frame_controles.pack_propagate(False)

        self.frame_grafica = ttk.Frame(self.root, padding=10)
        self.frame_grafica.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.configurar_interfaz_controles()
        self.inicializar_grafica()

        # Estado interno de la simulación
        self.ani          = None
        self._pasos_total = 0      # pasos de tiempo acumulados
        self._dt          = 1e-4   # se actualiza al lanzar la simulación

    # ==================================================================
    def configurar_interfaz_controles(self):
        lbl_titulo = ttk.Label(
            self.frame_controles,
            text="Parámetros de Simulación",
            font=("Arial", 14, "bold"),
        )
        lbl_titulo.pack(pady=(0, 10))

        # --- CONFIGURACIÓN INICIAL ---
        frame_global = ttk.LabelFrame(
            self.frame_controles, text=" Configuración Inicial ", padding=10
        )
        frame_global.pack(fill=tk.X, pady=(0, 8))

        self.var_atomico = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frame_global,
            text="Usar unidades atómicas/naturales (hbar=1, masa=1)",
            variable=self.var_atomico,
        ).pack(anchor=tk.W, pady=4)

        ttk.Label(frame_global, text="Seleccione el potencial:").pack(
            anchor=tk.W, pady=(4, 2)
        )
        lista_potenciales = [
            "libre", "pozo_infinito", "escalon", "barrera",
            "pozo_finito", "pozo_triangular", "oscilador_armonico", "doble_pozo",
        ]
        self.combo_potencial = ttk.Combobox(
            frame_global, values=lista_potenciales, state="readonly"
        )
        self.combo_potencial.set("doble_pozo")
        self.combo_potencial.pack(fill=tk.X, pady=4)

        # Velocidad de animación (pasos por frame)
        frame_vel = ttk.Frame(frame_global)
        frame_vel.pack(fill=tk.X, pady=4)
        ttk.Label(frame_vel, text="Pasos por frame:").pack(side=tk.LEFT)
        self.entry_pasos = ttk.Entry(frame_vel, width=6)
        self.entry_pasos.insert(0, "50")
        self.entry_pasos.pack(side=tk.LEFT, padx=(6, 0))
        ttk.Label(frame_vel, text="(↑ = más rápido)", foreground="gray").pack(
            side=tk.LEFT, padx=(6, 0)
        )

        # --- CUADRÍCULA DE PARÁMETROS ---
        frame_RECOPILACION = ttk.LabelFrame(
            self.frame_controles, text=" Parámetros del Sistema ", padding=10
        )
        frame_RECOPILACION.pack(fill=tk.BOTH, expand=True, pady=5)

        lista_parametros = [
            ("limite_izq", -0.2), ("limite_der",  0.2),
            ("V_0",        25.0), ("punto_potencial", 0.0),
            ("grillaI",   -15.0), ("grillaD",    15.0),
            ("N",          3000), ("dt",          0.0001),
            ("sigma",       1.0), ("k0",           5.0),
            ("x0",         -5.0), ("ancho",         3.0),
            ("fuerza",     15.0), ("omega",          1.0),
            ("centro_parabola", 0.0), ("valor_infinito", 1e10),
            ("centro",      0.0), ("epsilon",       0.3),
            ("lam",         0.1), ("a",             3.0),
        ]

        self.entradas_texto = {}
        for i, (nombre, defecto) in enumerate(lista_parametros):
            fila       = i // 2
            col_base   = (i % 2) * 2
            ttk.Label(frame_RECOPILACION, text=f"{nombre}:").grid(
                row=fila, column=col_base, sticky=tk.W, padx=(5, 2), pady=3
            )
            entry = ttk.Entry(frame_RECOPILACION, width=10)
            entry.insert(0, str(defecto))
            entry.grid(
                row=fila, column=col_base + 1, sticky=tk.EW, padx=(0, 10), pady=3
            )
            self.entradas_texto[nombre] = entry

        frame_RECOPILACION.columnconfigure(1, weight=1)
        frame_RECOPILACION.columnconfigure(3, weight=1)

        # --- BOTONES ---
        btn_frame = ttk.Frame(self.frame_controles)
        btn_frame.pack(fill=tk.X, pady=(8, 0))

        self.btn_graficar = ttk.Button(
            btn_frame, text="Calcular y Graficar", command=self.procesar_y_graficar
        )
        self.btn_graficar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_detener = ttk.Button(
            btn_frame, text="Detener", command=self.detener_animacion, state=tk.DISABLED
        )
        self.btn_detener.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- PANEL DE ESTADO (temporizador + normalización) ---
        frame_estado = ttk.LabelFrame(
            self.frame_controles, text=" Estado de la Simulación ", padding=8
        )
        frame_estado.pack(fill=tk.X, pady=(10, 0))

        # Temporizador
        fila_t = ttk.Frame(frame_estado)
        fila_t.pack(fill=tk.X, pady=2)
        ttk.Label(fila_t, text="Tiempo simulado:", width=18, anchor=tk.W).pack(
            side=tk.LEFT
        )
        self.var_tiempo = tk.StringVar(value="—")
        ttk.Label(fila_t, textvariable=self.var_tiempo, font=("Courier", 10, "bold")).pack(
            side=tk.LEFT
        )

        # Normalización
        fila_n = ttk.Frame(frame_estado)
        fila_n.pack(fill=tk.X, pady=2)
        ttk.Label(fila_n, text="‖ψ‖²:", width=18, anchor=tk.W).pack(side=tk.LEFT)
        self.var_norma = tk.StringVar(value="—")
        self.lbl_norma = ttk.Label(
            fila_n,
            textvariable=self.var_norma,
            font=("Courier", 10, "bold"),
            foreground="gray",
        )
        self.lbl_norma.pack(side=tk.LEFT)

        # Leyenda de colores de normalización
        fila_ley = ttk.Frame(frame_estado)
        fila_ley.pack(fill=tk.X, pady=(4, 0))
        for color, texto in [("green", "OK (<1%)"), ("goldenrod", "Leve (<5%)"), ("red", "Crítico (≥5%)")]:
            tk.Label(fila_ley, text="●", foreground=color).pack(side=tk.LEFT)
            ttk.Label(fila_ley, text=texto, foreground="gray").pack(side=tk.LEFT, padx=(0, 8))

    # ==================================================================
    def inicializar_grafica(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.ax.set_title("Función de Onda y Perfil de Potencial")
        self.ax.set_xlabel("Posición (x)")
        self.ax.set_ylabel(r"$|\psi|^2$")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafica)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ==================================================================
    def procesar_y_graficar(self):
        try:
            potencial_nombre = self.combo_potencial.get()

            if self.var_atomico.get():
                constantes = {"hbar": 1.0, "masa": 1.0}
            else:
                from tkinter import simpledialog
                masa_str = simpledialog.askstring(
                    "Masa", "Ingrese la masa en kg:", parent=self.root
                )
                masa_si  = float(masa_str) if masa_str else const.m_e
                constantes = {"hbar": const.hbar, "masa": masa_si}

            p = {}
            for nombre, entry in self.entradas_texto.items():
                valor = entry.get().strip()
                p[nombre] = int(valor) if nombre == "N" else float(valor)

            if p["limite_der"] <= p["limite_izq"]:
                messagebox.showerror(
                    "Error de parámetros",
                    "limite_der debe ser estrictamente mayor que limite_izq.",
                )
                return
            if p["grillaD"] <= p["grillaI"]:
                messagebox.showerror(
                    "Error de parámetros",
                    "grillaD debe ser estrictamente mayor que grillaI.",
                )
                return

            # Leer pasos por frame (con fallback seguro)
            try:
                self._pasos_por_frame = max(1, int(self.entry_pasos.get().strip()))
            except ValueError:
                self._pasos_por_frame = 50

            self.renderizar_simulacion(potencial_nombre, constantes, p)

        except ValueError:
            messagebox.showerror(
                "Error de formato",
                "Asegúrate de ingresar números válidos en todos los campos.",
            )

    # ==================================================================
    def renderizar_simulacion(self, potencial_nombre, constantes, p):
        self.detener_animacion()

        # Resetear contadores
        self._pasos_total = 0
        self._dt          = p["dt"]
        self.var_tiempo.set("t = 0.000000")
        self.var_norma.set("—")

        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel(r"$|\psi|^2$")

        dx = (p["grillaD"] - p["grillaI"]) / int(p["N"])
        x  = np.linspace(p["grillaI"] + dx, p["grillaD"] - dx, int(p["N"]))

        self.psi  = estado_inicial(x, dx, **p)
        self.dx   = dx
        self.x    = x
        self.p    = p

        pot    = c_potenciales()
        V_real = pot.potencial[potencial_nombre](x, **p)
        V      = agregar_absorbente(V_real, x, ancho=p["ancho"], fuerza=p["fuerza"])
        self.diags_AB = operador_evolucion_temporal(V, **p, **constantes)

        # Escalar V(x) para visualización
        V_visual  = np.real(V_real).astype(np.float64)
        v_abs_max = np.max(np.abs(V_visual))
        if v_abs_max > 0:
            V_visual = V_visual / v_abs_max * 0.3

        y_min = min(float(V_visual.min()) - 0.05, -0.05)
        y_max = 0.5

        self.ax.set_xlim(p["grillaI"], p["grillaD"])
        self.ax.set_ylim(y_min, y_max)

        self.ax.fill_between(x, V_visual, 0, where=(V_visual >= 0),
                             alpha=0.25, color="orange", label="V(x) > 0")
        self.ax.fill_between(x, V_visual, 0, where=(V_visual < 0),
                             alpha=0.25, color="green",  label="V(x) < 0")
        self.ax.plot(x, V_visual, color="darkorange", lw=1.0, alpha=0.7)
        self.ax.axhline(0, color="gray", lw=0.5, linestyle="--")

        (self.line,) = self.ax.plot(
            x, np.abs(self.psi) ** 2, color="royalblue", lw=1.5, label=r"$|\psi|^2$"
        )

        # Texto de temporizador y norma dentro del gráfico (esquina superior izquierda)
        self._txt_grafico = self.ax.text(
            0.02, 0.97, "",
            transform=self.ax.transAxes,
            fontsize=8, verticalalignment="top",
            fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
        )

        self.ax.legend(loc="upper right", fontsize=8)

        self.ani = animation.FuncAnimation(
            self.fig,
            self.actualizar_frame,
            interval=20,
            blit=False,
            cache_frame_data=False,
        )

        self.canvas.draw()
        self.btn_detener.config(state=tk.NORMAL)
        self.btn_graficar.config(state=tk.NORMAL)

    # ==================================================================
    def actualizar_frame(self, _frame):
        # --- Evolución temporal ---
        for _ in range(self._pasos_por_frame):
            self.psi = paso_tiempo(self.psi, *self.diags_AB)

        self._pasos_total += self._pasos_por_frame
        t_sim = self._pasos_total * self._dt

        # --- Normalización ---
        norma = float(np.sum(np.abs(self.psi) ** 2) * self.dx)
        desviacion = abs(norma - 1.0)

        if desviacion < _NORM_OK:
            color_norma = "green"
            estado_norma = "OK"
        elif desviacion < _NORM_WARN:
            color_norma = "goldenrod"
            estado_norma = "LEVE"
        else:
            color_norma = "red"
            estado_norma = "CRÍTICO"

        # Actualizar labels del panel lateral
        self.var_tiempo.set(f"t = {t_sim:.6f}")
        self.var_norma.set(f"{norma:.6f}  [{estado_norma}]")
        self.lbl_norma.config(foreground=color_norma)

        # Actualizar texto dentro del gráfico
        self._txt_grafico.set_text(
            f"t = {t_sim:.4f}\n‖ψ‖² = {norma:.5f}"
        )

        # Actualizar curva ψ
        self.line.set_ydata(np.abs(self.psi) ** 2)
        return (self.line,)

    # ==================================================================
    def detener_animacion(self):
        if self.ani is not None:
            self.ani.event_source.stop()
            self.ani = None
        self.btn_detener.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = GraficadoraEfectoTunel(root)
    root.mainloop()
