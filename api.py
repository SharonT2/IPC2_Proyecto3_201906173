from os import error, stat
from sys import version
from flask import Flask, Response, request
from flask_cors import CORS
from math import pow
import xml.etree.ElementTree as ET
from peticiones import Peticiones
import re
from datetime import datetime


variable=""
ver = ""
arreglo = []
con=False
con2=False
con3=False
con4=False
tres=""
cuatro=""
cErr=0
cErr2=0
x=1
rango=[]
rangox=[]

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
    global ver
    global arreglo
    global con
    global con2
    global con3
    global con4
    global tres
    global cuatro
    global cErr
    global cErr2
    global x
    global rango
    global rangox

    if request.data==b'':
        print("Respuesta de postman: ", variable)
        str_file = variable
        print("Ruta del archivo mandado desde postman: ", str_file)
    else:
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
                nitE()
            #----------------------------#3 Analizando el nit Receptor---------------------------------
            for rh in c.iter('NIT_RECEPTOR'):
                cuatro=rh.text.strip()
                #print("nitreceptor: ", r1.text.strip())
                nitR()
            #----------------------------#3 Analizando el valor---------------------------------
            for r1 in c.iter('VALOR'):
                cinco=r1.text.strip()
                cincoaux=cinco
                #print("valor: ", r1.text.strip())
                try:
                    valorniu=re.search(r"([0-9]+[.]+[0-9]{2})", cinco).group(0)#obtiene la cadena si está correcta
                    if valorniu == cinco:#compara si tiene la misma cantidad de decimales, ya que eso no da error
                            print("valor aceptado: ", cinco)#si es así lo acepta
                    else:
                            print("Valor no aceptado, tiene más de dos decimales: ", cinco)
                            cinco=cinco+"#"
                            print("Valor con numeral: ", cinco)
                            con=True#error que indicará para el objeto, por tener más de dos decimales
                except:
                        print("Valor no válido, sintaxis incorrecta: ", cinco)
                        cinco=cinco+"#"
                        print("Valor con numeral: ", cinco)
                        con=True#error que indicará para el objeto, por tener sintaxis incorrecta
            for r1 in c.iter('IVA'):
                seis=r1.text.strip()
                #print("iva: ", r1.text.strip())
                seisaux=seis
                
            for r1 in c.iter('TOTAL'):
                siete=r1.text.strip()
                #print("total: ", r1.text.strip())
            #------Calculando Iva*
            try:
                iva=(float(cincoaux)) * 0.12
                ivaRed=round(iva, 2)#redondeando el iva
                if float(ivaRed) == float(seis):#si el iva de resultado es igual al que me mandaron
                    print("IVA correcto: ", seis)
                else:
                    print("IVA incorrecto: ", seis)
                    seis=seis+"#"
                    print("IVA con numeral: ", seis)
                    con=True#error que indicará para el objeto, por tener iva mal calculado
            except:
                print("No se ha podido realizar calculo del iva formato de algun valor incorrecta: ", seis)
                print("IVA incorrecto, no se pudo realizar el calculo: ", seis)
                seis=seis+"#"
                print("IVA con numeral: ", seis)
                con=True#error que indicará para el objeto, por no poder calcular iva
            
            #------Calculando total*
            try:
                total = ((float(cincoaux)) * 0.12) + float(cincoaux)#sumé el iva y el valor original
                total = round(total, 2)#redondeo el total
                if float(total) == float(siete):#si el total de resultado es igual al que me mandaron
                    print("Total correcto: ", siete)
                else:
                    print("Total incorrecto, no es igual al que mandaron: ", siete)
                    siete=siete+"#"
                    print("Total con numeral: ", siete)
                    con=True#error que indicará para el objeto, por tener iva mal calculado
            except:
                print("No se ha podido realizar calculo del total, sintaxis de algun valor incorrecta: ", siete)
                print("Total incorrecto, no se pudo realizar el calculo: ", siete)
                siete=siete+"#"
                print("Total con numeral: ", siete)
                con=True#error que indicará para el objeto, por tener total sn calcular por tener datos con sintaxis erronea

            #-----Mandando datos al objeto
            print()
            arreglo.append(Peticiones(uno, dos, tres, cuatro, cinco, seis, siete, con))
            print("--------------------------------------------------------------------")
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

    
    for i in range(len(arreglo)):
        if arreglo[i].getCon() == False:#las ue no tengan errores
            try:
                fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[i].getTiempo()).group(0)#obtén cada fecha
                if fecha not in rango:#si no la he guardado antes
                    rango.append(fecha)
            except:
                print()
        
    for i in range(len(arreglo)):#almacenando todas las fechas
        if str(arreglo[i].getTiempo()[-1])!="#":#menos las fechas que tienen errores
            try:
                fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[i].getTiempo()).group(0)#obtén cada fecha
                rangox.append(fecha)
            except:
                print()

    #-----------------------------------------Escribiendo en archivo de salida-----
    #aquí masomenos terminaría de procesarlo
    #variable="ahorasí Prueba"
    fechaAc = datetime.today().strftime('%d/%m/%Y')
    archivo2 = open('modificación.xml', 'w+')#w+ será sobre escritura, borrará y volverá a escribirlo, hay que cambiar esto 
    archivo2.write("<LISTAAUTORIZACIONES>\n")

    
    for i in rango:
        archivo2.write("    <AUTORIZACION>\n")
        archivo2.write("        <FECHA>" + str(i)+ "</FECHA>\n")
        fr=rangox.count(i)#------>total recibidas
        cErr=0 
        for p0 in range(len(arreglo)):#------>errores en nit emisor
#            if arreglo[p0].getCon() == True:#las que tengan errores
            if str(arreglo[p0].getTiempo()[-1])!="#":#pero la fechas in error
                try:
                    fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[p0].getTiempo()).group(0)#obten la fecha en cada posicion
                    if i == fecha:#qeu tengan la misma fecha en la que estoy viendo
                        if str(arreglo[p0].getNitE()[-1])=="#":#si encuentra un error en nit emisor
                                cErr+=1#aumenta el contador
                except:
                    print()
        cErr2=0 
        for p1 in range(len(arreglo)):#------>errores en nit receptor
#            if arreglo[p1].getCon() == True:#las que tengan errores
            if str(arreglo[p1].getTiempo()[-1])!="#":#pero la fechas in error
                try:
                    fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[p1].getTiempo()).group(0)#obten la fecha en cada posicion
                    if i == fecha:#qeu tengan la misma fecha en la que estoy viendo
                        if str(arreglo[p1].getNitR()[-1])=="#":#si encuentra un error en nit receptor
                                cErr2+=1#aumenta el contador
                except:
                    print()
        cErr3=0 
        for p1 in range(len(arreglo)):#------>errores en iva
#            if arreglo[p1].getCon() == True:#las que tengan errores
            if str(arreglo[p1].getTiempo()[-1])!="#":#pero la fechas in error
                try:
                    fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[p1].getTiempo()).group(0)#obten la fecha en cada posicion
                    if i == fecha:#qeu tengan la misma fecha en la que estoy viendo
                        if str(arreglo[p1].getIva()[-1])=="#":#si encuentra un error en nit iva
                                cErr3+=1#aumenta el contador
                except:
                    print()
        cErr4=0 
        for p1 in range(len(arreglo)):#------>errores en total
            if str(arreglo[p0].getTiempo()[-1])!="#":#pero la fechas in error
                cadena=arreglo[p1].getTiempo()
                print(cadena)
                try:
                    fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", cadena).group(0)#obten la fecha en cada posicion
                    if i == fecha:#qeu tengan la misma fecha en la que estoy viendo
                        if str(arreglo[p1].getTotal()[-1])=="#":#si encuentra un error en total
                                cErr4+=1#aumenta el contador
                except:
                    print()
        cErr5=0 
        for p1 in range(len(arreglo)):#------>errores en rerferencia
#            if arreglo[p1].getCon() == True:#las que tengan errores
            if str(arreglo[p0].getTiempo()[-1])!="#":#pero la fechas in error
                try:
                    fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[p1].getTiempo()).group(0)#obten la fecha en cada posicion
                    if i == fecha:#qeu tengan la misma fecha en la que estoy viendo
                        if str(arreglo[p1].getReferencia()[-1])=="#":#si encuentra un error en referencia
                                cErr5+=1#aumenta el contador
                except:
                    print()
        cErr6=0 #facturas correctas
        for p1 in range(len(arreglo)):#------>
            if arreglo[p1].getCon() == False:#las que no tengan errores
                fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[p1].getTiempo()).group(0)#obten la fecha en cada posicion
                if i == fecha:#qeu tengan la misma fecha en la que estoy viendo
                    cErr6+=1
        cErr7=0#emisores correctos
        for p1 in range(len(arreglo)):#------>
            if str(arreglo[p1].getNitE()[-1])!="#":#si no hay error en emisores
                try:
                    fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[p1].getTiempo()).group(0)#obten la fecha en cada posicion
                    if i == fecha:#qeu tengan la misma fecha en la que estoy viendo
                        cErr7+=1
                except:
                    print()
        
        cErr7=0#receptores correctos
        for p1 in range(len(arreglo)):#------>
            if str(arreglo[p1].getNitR()[-1])!="#":#si no hay error en emisores
                try:
                    fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[p1].getTiempo()).group(0)#obten la fecha en cada posicion
                    if i == fecha:#qeu tengan la misma fecha en la que estoy viendo
                        cErr7+=1
                except:
                    print()
        
        cErr8=0#receptores correctos
        for p1 in range(len(arreglo)):#------>
            if str(arreglo[p1].getNitE()[-1])!="#":#si no hay error en emisores
                try:
                    fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[p1].getTiempo()).group(0)#obten la fecha en cada posicion
                    if i == fecha:#qeu tengan la misma fecha en la que estoy viendo
                        cErr8+=1
                except:
                    print()

        archivo2.write("        <FACTURAS_RECIBIDAS>" + str(fr)+ "</FACTURAS_RECIBIDAS>\n")
        archivo2.write("        <ERRORES>\n")
        archivo2.write("            <NIT_EMISOR>" + str(cErr) + "</NIT_EMISOR>\n")
        archivo2.write("            <NIT_RECEPTOR>" + str(cErr2) + "</NIT_RECEPTOR>\n")
        archivo2.write("            <IVA>" + str(cErr3) + "</IVA>\n")
        archivo2.write("            <TOTAL>" + str(cErr4) + "</TOTAL>\n")
        archivo2.write("            <REFERENCIA_DUPLICADA>" + str(cErr5) + "</REFERENCIA_DUPLICADA>\n")
        archivo2.write("        </ERRORES>\n")
        archivo2.write("        <FACTURAS_CORRECTAS>" + str(cErr6) + "</FACTURAS_CORRECTAS>\n")
        archivo2.write("        <CANTIDAD_EMISORES>" + str(cErr7) + "</CANTIDAD_EMISORES>\n")
        archivo2.write("        <CANTIDAD_RECEPTORES>" + str(cErr8) + "</CANTIDAD_RECEPTORES>\n")
        archivo2.write("        <LISTADO_AUTORIZACIONES>\n")

        for p in range(len(arreglo)):
            if arreglo[p].getCon() == False:#las ue no tengan errores
                fecha=re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", arreglo[p].getTiempo()).group(0)
                if i == fecha:
                    print("Igualdad: ", i, fecha)
                    r=8
                    año=re.search(r"(\d{4})", arreglo[p].getTiempo()).group(0)
                    mes=re.search(r"([-/]\d{2})", arreglo[p].getTiempo()).group(0)
                    mes=mes[1:]
                    dia=re.search(r"(\d{2})", arreglo[p].getTiempo()).group(0)
                    c=""#reseteo el codigo
                    r=r-len(str(x))
                    for j in range(r):
                        c=c+"0"
                    c=c+str(x)
                    #print("Correlativo: ", c)
                    codigo=año+mes+dia+c
                    x+=1#subo el correlativo
                    
                    archivo2.write("            <APROBACION>\n")
                    archivo2.write("                <NIT_EMISOR ref=\""+ str(arreglo[p].getReferencia()) + "\">" + str(arreglo[p].getNitE()) + "</NIT_EMISOR>\n")
                    archivo2.write("                <CODIGO_APROBACION>" + str(codigo) + "</CODIGO_APROBACION>\n")
                    archivo2.write("                <NIT_RECEPTOR"+ str(arreglo[p].getNitR()) + "</NIT_RECEPTOR>\n")
                    archivo2.write("                <VALOR>" + str(arreglo[p].getValor()) + "</VALOR>\n")
                    archivo2.write("            </APROBACION>\n")

        archivo2.write("            <TOTAL_APROBACIONES>" + str(cErr6) + "</TOTAL_APROBACIONES>\n")
        archivo2.write("        </LISTADO_AUTORIZACIONES>\n")
        archivo2.write("    </AUTORIZACION>\n")
        x=1

    archivo2.write("</LISTAAUTORIZACIONES>\n")
    archivo2.close()
    return Response(status=204)

@app.route('/leer', methods=['GET'])
def leer():
    #Desde aquí se podría leer para obtener solo los
    archivo = ET.parse('prueba.xml')
    raiz = archivo.getroot()
    print("Raiz: ", raiz)
    return("entra")

@app.route('/server', methods=['GET'])
def server():
    global variable
    global ver
    variable = "Sí entra"
    print(variable)
    variable = str(request.args.get('variable'))
    print(variable)
    return Response(variable)



#--------------------------------------------Método para poder analizar y validar el nit Emisor-------------------------------------


def nitE():
    global con
    global con3
    global arreglo
    global tres
    #try:
    if len(tres) <= 20:
##        #Verificando si el nit receptor ya se encuentra<----- 
##        for i in range(len(arreglo)):#busca en mi arreglo de objetos, si el nit emisor ya se encuentra
##            if str(tres)==str(arreglo[i].getNitE()):#si mi nit emisor que estoy obteniendo de mi archivo ya se encuentra registrado
##                #aqui podría ir el contador de cuántas veces se repite un nit emisor
##                if arreglo[i].getCon()==False:#y si este no contiene error alguno en todo su registro
##                    con=True#error que indicará para el objeto, por estar repetido el nit
##                    con3=True#indicara qeu mi nit ya se encuentra
##        if con3==False:#<-----Mientras mi nit no esté duplicado
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
##        else:
##            print("El nit es incorrecto por que ya se encuentra registrado: ", tres)
##            tres=tres+"#"#le agrega un numeral para poder representar su error
##            print("Con numeral: ", tres)#me la muestra con numeral
##            con=True#error que indicará para el objeto por error de verificador
    else:
        print("Este nit emisor contiene más de 20 caracteres: ", tres)
        tres=tres+"#"#agrego el error al nit para identificar
        print("NitEmisor con numeral: ", tres)
        con=True#error que indicará para el objeto, por tener más de 20 caracteres
    #except:
    #    print("FFFFFFFFFFFF")

#--------------------------------------------Método para poder analizar y validar el nit Receptor-------------------------------------

def nitR():
    global arreglo
    global con
    global con4
    global arreglo
    global cuatro
    #try:
    if len(cuatro) <= 20:
##        #Verificando si el nit receptor ya se encuentra<----- 
##        for i in range(len(arreglo)):#busca en mi arreglo de objetos, si el nit emisor ya se encuentra
##            if str(cuatro)==str(arreglo[i].getNitR()):#si mi nit emisor que estoy obteniendo de mi archivo ya se encuentra registrado
##                #aqui podría ir el contador de cuántas veces se repite un nit emisor
##                if arreglo[i].getCon()==False:#y si este no contiene error alguno en todo su registro
##                    con=True#error que indicará para el objeto, por estar repetido el nit
##                    con4=True#indicara qeu mi nit ya se encuentra
##        if con4==False:#<-----Mientras mi nit no esté duplicado
        try:
            nit=re.search(r"(^[0-9]+$)", cuatro).group(0)#obtiene la cadena si está correcta
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
                print("Hay un error en el nit receptor, no es aceptable su verificador: ", cuatro)#me la devuelve para mostrarla
                cuatro=cuatro+"#"#le agrega un numeral para poder representar su error
                print("Con numeral: ", cuatro)#me la muestra con numeral
                con=True#error que indicará para el objeto por error de verificador
            #print("Sigueeeeeeeeeeeeeeeeeeee")
        except: 
            print("Hay un error en el nit receptor, no es aceptable su sintaxis: ", cuatro)
            cuatro=cuatro+"#"#le agrega un numeral para poder representar su error
            print("Con numeral: ", cuatro)#me la muestra con numeral
            con=True#error que indicará para el objeto por error de verificador
##        else:
##            print("El nit es incorrecto por que ya se encuentra registrado: ", cuatro)
##            cuatro=cuatro+"#"#le agrega un numeral para poder representar su error
##            print("Con numeral: ", cuatro)#me la muestra con numeral
##            con=True#error que indicará para el objeto por error de verificador
    else:
        print("Este nit receptor contiene más de 20 caracteres: ", cuatro)
        cuatro=cuatro+"#"#agrego el error al nit para identificar
        print("Nit receptor con numeral: ", cuatro)
        con=True#error que indicará para el objeto, por tener más de 20 caracteres

@app.route('/borrar', methods=['GET'])
def borrar():
    global arreglo
    archivo2 = open('modificación.xml', 'w+')
    archivo2.close()
    print("antes: ", arreglo)
    for i in arreglo:
        print(i) 
        del i
    
    for i in arreglo:
        print("de: ", i) 
        del i
    for i in range(len(arreglo)):
        print("------------>Petición: ", i)
        print("Tiempo: ", arreglo[i].getTiempo())
        print("Referencia: ", arreglo[i].getReferencia())
        print("NitE: ", arreglo[i].getNitE())
        print("NitR: ", arreglo[i].getNitR())
        print("Valor: ", arreglo[i].getValor())
        print("IVA: ", arreglo[i].getIva())
        print("Total: ", arreglo[i].getTotal())
        print("Eliminar: ", arreglo[i].getCon())


    del arreglo[:]
    print("queda: ", arreglo)
    return("Base de datos formateada")


if __name__=="__main__":
    app.run(debug=True)


#LA API EN PUERTO 5000