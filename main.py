from peticiones import Peticiones
variable=""
arreglo = []

arreglo.append(Peticiones("uno", "dos", "tres", "cuatro", "cinco", "seis", "siete"))

for i in range(len(arreglo)):
    print(arreglo[i].getTiempo())
