from os import error, stat
from flask import Flask, Response, request
from flask_cors import CORS
from math import pow
import xml.etree.ElementTree as ET
from peticiones import Peticiones
import re
from datetime import datetime

variable=""
ver=False
arreglo = []
con=False
con2=False
con3=False
tres=""

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

    archivo = open('archivo.xml', '+r')#abrimos el archivo, r+ modo lectura, el 'archivo.txt', es el nombre del archivo cono tal
    return Response(status=200, #indica que mandará una respuesta
                    response=archivo.read(), #leerá el archivo mandado
                    content_type='text/plain')#ese archivo será un texto plano

#PARA GUARDAR DATOS EN EL ARCHIVO
@app.route('/datos', methods=['POST'])#P1
def post_datos():
    global variable
    global arreglo
    global con
    global con2
    global con3
    global ver
    global tres
    
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
    print("------------DATOS DE LAS PETICIONES Y SUS POSIBLES ERRORES---------")
    uno=""
    dos=""
    tres=""
    cuatro=""
    cinco=""
    seis=""
    siete=""
    for r0 in raiz:
        for c in r0.iter('DTE'):#cantidad de linas de producción
            #-----------------------#1 Analizando la fecha con el tiempo---------------------------------
            for r1 in c.iter('TIEMPO'):
                uno=r1.text.strip()
                #print("tiempo: ", r1.text.strip())
                try:
                    re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4}\s\d{1,2}:\d{1,2})", uno).group(0)
                                #   dd    /    mm   /   yyyy 
                    print("Fecha correcta: ", uno)
                except:
                    print("Fecha con sintaxis incorrecta", uno)
                    uno=uno+"#"
                    print("con numeral: ", uno)
                    con=True
            #--------------------------#2 Analizando la referencia------------------------------------------
            for r1 in c.iter('REFERENCIA'):
                dos=r1.text.strip()
                #print("referencia: ", r1.text.strip())
                if len(dos)<=40:#si tiene la cantidad de digitios permitidos(maximo 40) se acepta
                    for i in range(len(arreglo)):#busca en mi arreglo de objetos, si la referencia ya se encuentra
                        if dos==arreglo[i].getReferencia():#si mi referencia que estoy obteniendo de mi archivo ya se encuentra registrada
                            buscar = re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[i].getTiempo()).group(0)#obten su fecha, sin la hora
                            for j in range(len(arreglo)):#vuelve a guscar en mi arreglo de objetos
                                buscar2 = re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[j].getTiempo()).group(0)#y obtiene cada fecha con forme vaya pasando
                                if buscar == buscar2:#si la fecha también está repetida, descárta la referencia
                                    con2=True#confirma qeu está repetida
                                    print("referencia", dos ," descartada por contener la misma referencia en la misma fecha")
                                    dos=dos+"#"
                                    print("Referencia con numeral: ", dos)
                                    con=True#error que indicará para el objeto, por estar duplicada
                        #else:
                            #con2=False#si no falso de nuevo
                    if con2==False:#mientras no esté duplicada
                        try:#revisa la referencia
                            referencia = re.match("^[A-Za-z0-9]*$", dos).group(0)#con la expresión regular
                            print("Referencia correcta: ", referencia)#la devuelve si todo sale bien
                        except:#si encuentra algo que no es aceptable
                            print("Hay un error en la referencia: ", dos)#me la devuelve para mostrarla
                            dos=dos+"#"#le agrega un numeral para poder representar su error
                            print("Con numeral: ", dos)#me la muestra con numeral
                            con=True#error que indicará para el objeto por error de sintaxis
                else:
                    print("Esta referencia tiene más de 40 caracteres: ", dos)
                    dos=dos+"#"#agrego el error a la referencia par identificar
                    print("Referencia con numeral: ", dos)
                    con=True#error que indicará para el objeto, por tener más de 40 caracteres

            #----------------------------#3 Analizando el nit Emisor---------------------------------
            for r1 in c.iter('NIT_EMISOR'):
                tres=r1.text.strip()
                #print("nitemisor: ", r1.text.strip())
                borrador()
            for rh in c.iter('NIT_RECEPTOR'):
                cuatro=rh.text.strip()
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
            arreglo.append(Peticiones(uno, dos, tres, cuatro, cinco, seis, siete, con))
            print()
            con=False#justo después de mandar la primera petición que va antes yo la vuelvo falsa para volver a iniciar
            con2=False
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
        print("Eliminar: ", arreglo[i].getCon())#si es true sí la descarta, si es false no la descarta

    
    #aquí masomenos terminaría de procesarlo
    variable="ahorasí Prueba"
    
    archivo2 = open('modificación.xml', 'w+')#w+ será sobre escritura, borrará y volverá a escribirlo
    archivo2.write(str_file)#esa variable la manda a escribir en un archivo 
    archivo2.close()
    return Response(status=204)

@app.route('/leer', methods=['GET'])
def leer():
    #Desde aquí se podría leer para obtener solo los
    archivo = ET.parse('prueba.xml')
    raiz = archivo.getroot()
    print("Raiz: ", raiz)
    return("entra")

def borrador():
    global arreglo
    global con
    global con3
    global arreglo
    global tres
    #try:
    if len(tres) <= 20:
        #Verificando si el nit receptor ya se encuentra<----- 
        for i in range(len(arreglo)):#busca en mi arreglo de objetos, si el nit emisor ya se encuentra
            if str(tres)==str(arreglo[i].getNitE()):#si mi nit emisor que estoy obteniendo de mi archivo ya se encuentra registrado
                #aqui podría ir el contador de cuántas veces se repite un nit emisor
                if arreglo[i].getCon()==False:#y si este no contiene error alguno en todo su registro
                    con=True#error que indicará para el objeto, por estar repetido el nit
                    con3=True#indicara qeu mi nit ya se encuentra
        if con3==False:#<-----Mientras mi nit no esté duplicado
            try:
                nit=re.search(r"(^[0-9]+$)", tres).group(0)#obtiene la cadena si está correcta
                #verificando nit<--------
                car=len(nit)#obteniendo la cantidad de caracteres
                car=car-2#le quito una posición por que le primero no cuenta
                c=car
                c2=2
                
                suma=0
                for i in nit:
                    if c>=0:#mientras no estés en la posición del primero de derecha a izquerda <---
                        x=int(nit[c])*c2#multiplica por su posición
                        #print(nit[c], c2, "= ", x )#imprimi,
                        suma=suma+x#sumar los resultados de las multiplicacionies
                        c2+=1
                        c=c-1
                mod=suma%11#primer mod a la suma
                v=11-mod#le resto a 11 el primer mod
                k=v%11#a la resta anterior le aplico también el mod
                if k==int(nit[-1]):#si el mod obtenido, es iugal al digito con el que tengo que verigicarlo, entonces aceptalo
                    print("El nit: ", nit, " es válido VERIFICADO")
                else:
                    print("Hay un error en el nit emisor, no es aceptable su verificador: ", tres)#me la devuelve para mostrarla
                    tres=tres+"#"#le agrega un numeral para poder representar su error
                    print("Con numeral: ", tres)#me la muestra con numeral
                    con=True#error que indicará para el objeto por error de verificador
                #print("Sigueeeeeeeeeeeeeeeeeeee")
            except:
                print("Hay un error en el nit emisor, no es aceptable su sintaxis: ", tres)
                tres=tres+"#"#le agrega un numeral para poder representar su error
                print("Con numeral: ", tres)#me la muestra con numeral
                con=True#error que indicará para el objeto por error de verificador
        else:
            print("El nit es incorrecto por que ya se encuentra registrado: ", tres)
            tres=tres+"#"#le agrega un numeral para poder representar su error
            print("Con numeral: ", tres)#me la muestra con numeral
            con=True#error que indicará para el objeto por error de verificador
    else:
        print("Este nit emisor contiene más de 20 caracteres: ", tres)
        tres=tres+"#"#agrego el error al nit para identificar
        print("NitEmisor con numeral: ", tres)
        con=True#error que indicará para el objeto, por tener más de 20 caracteres
    #except:
    #    print("FFFFFFFFFFFF")

if __name__=="__main__":
    app.run(debug=True)


#LA API EN PUERTO 5000