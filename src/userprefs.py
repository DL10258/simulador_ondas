class user_config:
    def __init__(self):
        self.params={
            "limite_izq":-0.2,
            "limite_der":0.2,
            "V0":25.0,
            "punto_potencial":0.0,
            "dt":1e-4,
            "sigma":1.0,
            "k0":5.0
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
