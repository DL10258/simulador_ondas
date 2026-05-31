import scipy.constants as const
class user_config:
    def __init__(self):
        self.params={
            "limite_izq":-0.2,
            "limite_der":0.2,
            "V_0":25.0,
            "punto_potencial":0.0,
            "grillaI":-15.0,
            "grillaD":15.0,
            "N":3000,
            "dt":1e-4,
            "sigma":1.0,
            "k0":5.0,
            "x0":-5.0,
            "ancho":3.0,
            "fuerza":15.0,
            "omega":1.0,
            "centro_parabola":0.0,
            "valor_infinito":1e10,
            "centro":0.0,
            "epsilon":0.3,
            "lam":0.1,
            "a":3.0
        }
    def obtener_datos(self):
        for p in self.params:
            while True:
                try:
                    entrada=input(f"Ingrese el {p} (default: {self.params[p]}): ").strip()
                    if entrada=="":
                        valor_evaluar=self.params[p] 
                    else:
                        valor_evaluar=float(entrada)
                    if p=="limite_der":
                        if valor_evaluar<=self.params["limite_izq"]:
                            print(f"Error: El limite_der ({valor_evaluar}) debe ser mayor que el limite_izq ({self.params['limite_izq']}).")
                            continue
                    if p=="N":
                        self.params[p]=int(valor_evaluar)
                    else:
                        self.params[p]=valor_evaluar
                    break 
                except ValueError:
                    print("Error: Ingrese un valor numérico válido por favor.")
    def datos_elegidos(self):
        return self.params 
    def validar_datos(self):
        if self.params["limite_izq"]>=self.params["limite_der"]:
            raise ValueError("El limite derecho debe de ser mayor estrictamente al izquierdo")
    def datos_operador_temporal(self):
        return [int(self.params["N"]),self.params["dt"]]
    def datos_potencial(self):
            return {
        "limite_izq": self.params["limite_izq"],
        "limite_der": self.params["limite_der"],
        "V_0": self.params["V_0"],
        "punto_potencial": self.params["punto_potencial"]
    }


class constantes_elegidas:
    def __init__(self):
        self.constantes={
            "hbar":1.0,
            "masa":1.0}
    def obtener_datosc(self):
        opciones_positivas=["s","S","si","Si","SI","y","Y","yes","Yes","YES"]
        opciones_negativas=["n","N","no","No","NO"]
        while True:
            try:
                dato=input("¿Desea usar el sistema atomico? S/n: ")
                if dato in opciones_positivas:
                    break
                elif dato in opciones_negativas:
                    print("Se procedera a usar las constantes en el S.I.")
                    self.constantes["hbar"]=const.hbar
                    self.constantes["masa"]=float(input("Ingrese la masa: "))
                    break
                else:
                    print("Seleccione una opción valida por favor.")
            except:
                print("Seleccione una opcion valida.")

from potenciales import *
class c_potenciales:
    def __init__(self):
        self.potencial={
            "libre":libre,
            "pozo_infinito":pozo_infinito,
            "escalon":escalon,
            "barrera":barrera,
            "pozo_finito":pozo_finito,
            "pozo_triangular":pozo_triangular,
            "oscilador_armonico":oscilador_armonico,
            "doble_pozo":doble_pozo
        }
        self.absorbente=agregar_absorbente
    def selector(self,nombre):
        if nombre not in self.potencial:
            raise KeyError(f"El potencial {nombre} no se encuentra indexado en la base de datos")
        return self.potencial[nombre]
    def muestrame(self):
        for k,n in enumerate(self.potencial):
            print(f"{k}.{n}\n")
        while True:
            try:
                nombre=input("Copia el nombre tal cual por favor: ")
                if nombre not in self.potencial:
                    raise KeyError(f"El potencial {nombre} no se encuentra indexado en la base de datos, elige una opcion valida")
                break  
            except:
                print("Selecciona una opcion valida")
        return nombre
