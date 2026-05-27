import numpy as np 
from solver import paso_tiempo

def obtener_datos():
    print("INGRESAR DATOS PARA LA SIMULACIÓN\n")
    datos={}
    datos["limite_izq"]=float(input("Limite izquierdo: "))
    datos["limite_der"]=float(input("Limite derecho: "))
    datos["v0"]=float(input("V0: "))
    return datos 
user_config=obtener_datos()



