from os import stat
from flask import Flask, Response, request
from flask_cors import CORS
from math import pow
import xml.etree.ElementTree as ET
from peticiones import Peticiones
variable=""
arreglo = []

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})#permite que pueda acceder a mi api, desde direccioens externas etc.

@app.route('/')
def index():
    return "Hola mundo sí funciona el backend"

@app.route('/ruta1')
def ruta_1():
    return "ruta1"

@app.route('/ruta2')
def ruta_2():
    return "ruta2"

@app.route('/ruta3')
def ruta_3():
    return "ruta3"

#PARA QEU ME DEVUELVA LO QUE TENGO EN EL ARCHIVO 
@app.route('/datos', methods=['GET']) #P2
def get_datos():

    archivo = open('archivo.xml', '+r')#abrimos el archivo, r+ modo lectura, el 'archivo.txt', es el nombre del archivo como tal
    return Response(status=200, #indica que mandará una respuesta
                    response=archivo.read(), #leerá el archivo mandado
                    content_type='text/plain')#ese archivo será un texto plano

#PARA GUARDAR DATOS EN EL ARCHIVO
@app.route('/datos', methods=['POST'])#P1
def post_datos():
    global variable
    global arreglo
    print("RESPUESTA api: ", request.data)
    #print(request.data)
    #print("DOCS: ", request.docs)
    #modifiqué acá que me mandara solo la ruta pra que yo la lea con el xml
    str_file = request.data.decode('utf-8')#recibe los datos desde el frontend y lo almacena en una variable
    print("Ruta del archivo mandado desde el frontend", str_file)

#--------------------------aquí empieza xml---------------------
    archivo = ET.parse(str_file)#mando la ruta
#   print("archivo: ", archivo)
    raiz = archivo.getroot()
#    print("raiz: ", raiz)
    print("------------DATOS DE LAS PETICIONES---------")
    uno=""
    dos=""
    tres=""
    cuatro=""
    cinco=""
    seis=""
    for r0 in raiz:
        for c in r0.iter('DTE'):#cantidad de linas de producción
            for r1 in c.iter('TIEMPO'):
                uno=r1.text.strip()
                #print("tiempo: ", r1.text.strip())
            for r1 in c.iter('REFERENCIA'):
                dos=r1.text.strip()
                #print("referencia: ", r1.text.strip())
            for r1 in c.iter('NIT_EMISOR'):
                tres=r1.text.strip()
                #print("nitemisor: ", r1.text.strip())
            for r1 in c.iter('NIT_RECEPTOR'):
                cuatro=r1.text.strip()
                #print("nitreceptor: ", r1.text.strip())
            for r1 in c.iter('VALOR'):
                cinco=r1.text.strip()
                #print("valor: ", r1.text.strip())
            for r1 in c.iter('IVA'):
                seis=r1.text.strip()
                #print("iva: ", r1.text.strip())
            for r1 in c.iter('TOTAL'):
                siete=r1.text.strip()
                #print("total: ", r1.text.strip())
            arreglo.append(Peticiones(uno, dos, tres, cuatro, cinco, seis, siete))
            #print("--------->Petición: ")
            #aquí debe ir lo de imprimir los objetos ya los hice en un aarchivo a parte y sí imprime
    for i in range(len(arreglo)):
        print("------------>Petición: ", i)
        print("Tiempo: ", arreglo[i].getTiempo())
        print("Referencia: ", arreglo[i].getReferencia())
        print("NitE: ", arreglo[i].getNitE())
        print("NitR: ", arreglo[i].getNitR())
        print("Valor: ", arreglo[i].getValor())
        print("IVA: ", arreglo[i].getIva())
        print("Total: ", arreglo[i].getTotal())

    
    #aquí masomenos terminaría de procesarlo
    variable="ahorasí Prueba"
    
    archivo2 = open('modificación.xml', 'w+')#w+ será sobre escritura, borrará y volverá a escribirlo
    archivo2.write(str_file)#esa variable la manda a escribir en un archivo 
    archivo2.close()
    return Response(status=204)

@app.route('/prueba', methods=['GET'])
def prueba():
    global variable
    print(variable)
    return Response(variable)



@app.route('/potencia', methods=['GET'])
def potencia():
    n1 = int(request.args.get('n1'))
    n2 = int(request.args.get('n2'))
    return str(int(pow(n1, n2)))


@app.route('/leer', methods=['GET'])
def leer():
    #Desde aquí se podría leer para obtener solo los
    archivo = ET.parse('prueba.xml')
    raiz = archivo.getroot()
    print("Raiz: ", raiz)
    return("entra")


if __name__=="__main__":
    app.run(debug=True)


#LA API EN PUERTO 5000