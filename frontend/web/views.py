from django.shortcuts import redirect, render
import requests


#from api import potencia #me permitirá conectar la api
# Create your views here.

endpoint = 'http://localhost:5000{}' #variable corriendo en el puerto 5000

arreglo=[]

def index(request):
    if request.method == 'GET':
        url = endpoint.format('/datos')#manda a las llaves anteriores, el valor que se le pase,  desde endoint es como poner http://localhost:5000
        data = requests.get(url) #consulta a la api, el .get indica que irá al método que sea get y ese ejecutará
        print("DATA: ")
        print(data)
        #probando qeu mi frontend recibe los datos desde mi api
        url = endpoint.format('/prueba')
        data2 = requests.get(url)

        #Aquí podría mandar mi otra url qeu me cargue el archivo ya procesado y modificado
        #estoy pensando en hacer todo el xml procesado desde acá, osea recibo mi objeto ya modificado
        #con los datos aprobados, y desde aquí escribo mi archivo de modificación
        #otra opción sería abrir como tal el archivo desde aquí(qeu ya escribí en la api)
        #e imprimirlo en el index

        archivo = open('C:/Users/Sharon/Desktop/Proyecto3/modificación.xml', '+r')
        archivo=archivo.read()
        print("Archivo frontend: ", archivo)
        
        fecha=['fecha1', 'fecha2', 'fecha3']

        #el objeto data contiene la info y la pasa en un json
        context = {#diccionario
            'data': data.text, #.text par aenviar el texto como tal
            'data2': data2.text,
            'archivo': archivo,
            'fecha1': fecha,
        }
        return render(request, 'index.html', context)
    
    elif request.method == 'POST':
        docs = request.FILES['document']#desde aquí ese "document" es el que tengo desde la plantilla index.html
        print("RUTA DESDE POOOOOOOOOOOST RUTAAAAAAAAAAAAAAAAAAAAAAAA", docs)
        #data = docs.read()
        data = str(docs)#lo puse en str por que quiero mandar solo la url para que alla pruebe hacer las validaciones
        #si no lo ponía en string, entonces me mandaba el contenido del archivo como tal 
        url = endpoint.format('/datos') #el endpoint hace referencia a mi url, conectando así la api y la guarda en url
        requests.post(url, data) #url de la api, y el data es el contenido de mi archivo como tal
        return redirect('index')#me devolverá al mismo método index para recargar por get

def prueba(request):
    return redirect('hola')

def reporte():
    global arreglo