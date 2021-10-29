class Peticiones:
    def __init__(self, tiempo, referencia, nitE, nitR, valor, iva, total):#3l init es nuestro constructor
        self.tiempo = tiempo
        self.referencia = referencia
        self.nitE = nitE
        self.nitR = nitR
        self.valor = valor
        self.iva = iva
        self.total = total

#get
    def getTiempo(self):
        return self.tiempo
    
    def getReferencia(self):
        return self.referencia
    
    def getNitE(self):
        return self.nitE

    def getNitR(self):
        return self.nitR
    
    def getValor(self):
        return self.valor
    
    def getIva(self):
        return self.iva

    def getTotal(self):
        return self.total

#set
    def setTiempo(self, tiempo):
        self.tiempo = tiempo
    
    def setReferencia(self, referencia):
        self.referencia = referencia
    
    def setNitE(self, nitE):
        self.nitE = nitE
    
    def setNitR(self, nitR):
        self.nitR = nitR
    
    def setValor(self, valor):
        self.valor = valor
    
    def setIva(self, iva):
        self.iva = iva
        
    def setTotal(self, total):
        self.total = total
