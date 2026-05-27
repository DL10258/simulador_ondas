import numpy as np 
from solver import paso_tiempo

try:
    while True:
        seleccion=int(input('1.Pozo infinito, 2.Barrera, 3.Pozo finito, 4.Escalon'))
        if seleccion in [1,2,3,4]:
            break
        else:
            print('Selecciona una opción valida')
except:
    print('Error aun desconocido')

