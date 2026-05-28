class user_config:
    def __init__(self):
        self.params={
            "limite_izq":-0.2,
            "limite_der":0.2,
            "V0":25.0,
            "punto_potencial":0.0,
            "grilla":25.0,
            "N":1500,
            "dt":1e-4,
            "sigma":1.0,
            "k0":5.0,
            "x0":-5.0
        }
    def obtener_datos(self):
        for p in self.params:
            while True:
                try:
                    entrada = input(f"Ingrese el {p} (default: {self.params[p]}): ")
                    if entrada.strip() == "":
                        break  # mantiene el default y avanza
                    dato = float(entrada)
                    self.params[p] = int(dato) if p == "N" else dato
                    break
                except ValueError:
                    print('Ingresa un valor valido por favor.')
    def datos_elegidos(self):
        return self.params 
    def validar_datos(self):
        if self.params["limite_izq"]>=self.params["limite_der"]:
            raise ValueError("El limite derecho debe de ser mayor estrictamente al izquierdo")
    def datos_operador_temporal(self):
        return [int(self.params["N"]),self.params["grilla"],self.params["dt"]]
    def datos_potencial(self):
            return {
        "limite_izq": self.params["limite_izq"],
        "limite_der": self.params["limite_der"],
        "V_0": self.params["V0"],
        "punto_potencial": self.params["punto_potencial"]
    }


class constantes_elegidas:
    def __init__(self):
        self.constantes={
            "hbar":1.0,
            "masa":1.0}
    def obtener_datosc(self):
        for d in self.constantes:
            while True:
                try:
                    entrada = input(f"Ingrese el {d} (default: {self.constantes[d]}): ")
                    if entrada.strip() == "":
                        break
                    valor = float(entrada)
                    if valor <= 0:
                        print("El valor debe ser positivo.")
                        continue
                    self.constantes[d] = valor
                    break
                except ValueError:
                    print("Ingrese un valor valido por favor.")
    def validacion(self):
        if not all(map(lambda x:x>0,self.constantes.values())):
            raise ValueError("Todos los valores deben de ser estrictamente positivos")
    def datos_operador_temporal(self):
        return [self.constantes["hbar"],self.constantes["masa"]]

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
