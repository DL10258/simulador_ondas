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
                    dato=float(input(f"Ingrese el {p}: "))
                    if dato:
                        self.params[p]=dato
                    break
                except:
                    print('Ingresa un valor valido o deja vacio el valor por favor.')
    def datos_elegidos(self):
        return self.params 
    def validar_datos(self):
        if self.params["limite_izq"]>=self.params["limite_der"]:
            raise ValueError("El limite derecho debe de ser mayor estrictamente al izquierdo")
    def datos_operador_temporal(self):
        return [int(self.params["N"]),self.params["grilla"],self.params["dt"]]
    def datos_potencial(self):
        return [self.params["limite_izq"],self.params["limite_der"],self.params["V0"]]
class constantes_elegidas:
    def __init__(self):
        self.constantes={
            "hbar":1.0,
            "masa":1.0}
    def obtener_datosc(self):
        for d in self.constantes:
            while True:
                try:
                    valor=float(input(f"Ingrese el dato {d}: "))
                    if valor:
                            self.constantes[d]=valor 
                    break 
                except:
                    print("Ingrese un valor valido o deje la opcion vacia por favor.")
    def validacion(self):
        if not all(map(lambda x:x>0,self.constantes.values())):
            raise ValueError("Todos los valores deben de ser estrictamente positivos")
    def datos_operador_temporal(self):
        return [self.constantes["hbar"],self.constantes["masa"]]

from potenciales import *
class c_potenciales:
    def __init__(self):
        self.potencial={
            "pozo_infinito":pozo_infinito,
            "escalon":escalon,
            "barrera":barrera,
            "pozo_finito":pozo_finito
        }
    def selector(self,nombre):
        if nombre not in self.potencial:
            raise KeyError(f"El potencial {nombre} no se encuentra indexado en la base de datos")
        return self.potencial[nombre]
    def muestrame(self):
        for n in self.potencial:
            k=1
            print(f"{k}.{n}\n")
            k+=1
        while True:
            try:
                nombre=input("Copia el nombre tal cual por favor: ")
                if nombre not in self.potencial:
                    raise KeyError(f"El potencial {nombre} no se encuentra indexado en la base de datos, elige una opcion valida")
                break  
            except:
                print("Selecciona una opcion valida")
        return nombre
