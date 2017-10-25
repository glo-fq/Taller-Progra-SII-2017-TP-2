def principal():
    from datetime import datetime
    import os
    #import numpy
    import time
    import sys
    from scipy import misc
    tiempoInicio = time.clock() 

    matrizA = Matriz([[25, 144, 1, 9, 4], [25, 4, 9, 1, 16], [9, 1, 4, 9, 1], [16, 9, 4, 1, 9], [1, 25, 36, 25, 9]])

    #Ejemplo de clase de funcion rectángulo
    matrizB = Matriz([[0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0]])
    print(matrizA.__str__())
    f = matrizA.calcularImagenIntegral()
    conv = matrizA.filtrarPromediado(3)
    #g = Filtro(sys.argv, datetime, os)
    print("f: ", f)
    print("conv: ", conv)
		
    #print((time.clock() - tiempoInicio) * 10 ** 3, "ms") 



class Filtro:
    #Pedir sys.argv como parámetro en argumentos
    def __init__(self, argumentos, datetime, os):
        
        #Define el archivo que se va a analizar
        self.__archivoEntrada = self.encontrarArchivoEntrada(os)
        #Encuentra el método que se especificó
        self.__metodo = self.definirMetodo(argumentos)
        #Define el ancho de ventana
        self.__anchoVentana = self.definirAnchoVentana(argumentos)
        #Defune el nombre que tendrá el archivo 
        self.__nombreSalida = self.definirNombreArchivoSalida(argumentos, datetime.now())
    
    def encontrarArchivoEntrada(self, os):
        rutaImagenEntrada = input("Por favor escriba la ruta del archivo al que desea aplicar el filtro: ")
        nombreArchivoEntrada = input("Escriba el nombre del archivo a leer: ")
        directorioRutaRecibida = os.listdir(rutaImagenEntrada)
        posicionArchivo = nombreArchivoEntrada.index(directorioRutaRecibida)
        return directorioRutaRecibida[posicionArchivo]
        
    
    def definirMetodo(self, argumentos):
        #Se retorna el valor que se indique luego del argumento "-m"
        metodoAUtilizar = argumentos[argumentos.index("-m") + 1]
        return metodoAUtilizar
    
    def definirAnchoVentana(self, argumentos):
        ancho = argumentos[argumentos.index("-v") + 1]
        #Si encuentra el siguiente parámetro, esto indica que no se especificó el ancho de ventana
        if (ancho == "-m"):
            ancho = 3
        return ancho

    
    def definirNombreArchivoSalida(self, argumentos, instante):
        try:
            nombreArchivo = argumentos[argumentos.index("-o") + 1]
            if (nombreArchivo != "-v"):
                return nombreArchivo
            else:
                return ("%s_%s_%s_%s_%s_%s.bmp" % (instante.day, instante.month, instante.year, instante.hour, instante.minute, instante.second))
        except:
            return ("%s_%s_%s_%s_%s_%s.bmp" % (instante.day, instante.month, instante.year, instante.hour, instante.minute, instante.second))
            
    

class Matriz:
	
    """
    Se construye la matriz
    @param listaDeListas, la matriz recibida en forma de lista de listas
    @param numFilas, cantidad de filas de la matriz
    @param numColumnas, cantidad de columnas de la matriz
    @return la instancia de la matriz
    """
    def __init__(self, listaDeListas, numFilas = 0, numColumnas = 0):
        if(listaDeListas != []):
            self.__listaDeListas = listaDeListas
            self.__filas = len(listaDeListas)
            self.__columnas = len(listaDeListas[0])
            print("Se creó una matriz convencional.")
            
        else:
            self.__listaDeListas = self.inicializarConCeros(numFilas, numColumnas)
            self.__filas = numFilas
            self.__columnas = numColumnas
            #self.inicializarConCeros(numFilas, numColumnas)
            print("Se creó una matriz con ceros.")


    """Inicializa una matriz de ceros"""
    def inicializarConCeros(self, numFilas, numColumnas):
        import numpy
        self.__filas = numFilas
        self.__columnas = numColumnas
        self.__listaDeListas = []
        return numpy.zeros((numFilas, numColumnas))

    def setListaDeListas(self, listaDeListas):
    	self.__listaDeListas = listaDeListas
    	self.__filas = len(listaDeListas)
    	self.__columnas = len(listaDeListas[0])

    #retorna la matriz
    def getListaDeListas(self):
    	return self.__listaDeListas

    def setValor(self, fila, columna, valor):
    	self.__listaDeListas[fila][columna] = valor
        

    #retorna el valor
    def getValor(self, fila, columna):
    	return self.__listaDeListas[fila][columna]

    def __str__(self):
        hilera = str(self.__listaDeListas)
        hileraConInformacion = "Matriz: " + str(self.__listaDeListas) + "\n Numero de filas: " + str(self.__filas) + "\n Numero de columnas: " + str(self.__columnas)
        return hileraConInformacion

    def calcularPromedio(self):
        return self.calcularPromedioAux(0, 0)

    def calcularPromedioAux(self, filaActual, columnaActual):
        #Si está en medio de la fila, va realizando el promediado
        #Divide el valor actual entre la cant. de elementos y sigue con la sig. columna
        if(filaActual < self.__filas and columnaActual < self.__columnas):
            return self.__listaDeListas[filaActual][columnaActual] / (self.__filas * self.__columnas) + self.calcularPromedioAux(filaActual, columnaActual + 1)
        #Si ya se pasó del final de la fila pero no ha llegado al final de las filas,
        #sigue con la siguiente fila
        elif(filaActual < self.__filas and columnaActual == self.__columnas):
            return self.calcularPromedioAux(filaActual + 1, 0)
        #Si se pasó del final de la matriz, retorna 0
        else:
            return 0

    def filtrarPromediado(self, tamVentana):
        #Crea una matriz de ceros
        resultado = Matriz([], self.__filas, self.__columnas)
        return self.filtrarPromediadoAux(tamVentana, resultado, 0, 0)

    def filtrarPromediadoAux(self, tamVentana, resultado, filaActual, columnaActual):
        #El radio se saca a partir del tam. de ventana
        radio = tamVentana // 2
        #Cuando no se ha llegado al final
        if(filaActual < self.__filas and columnaActual < self.__columnas):
            #Caso de estar en un extremo: Se toma el valor original que tenía el pixel
            if((columnaActual - radio < 0) or (columnaActual + radio > self.__columnas) or (filaActual - radio < 0) or (filaActual + radio > self.__filas)):
                promedio = self.__listaDeListas[filaActual][columnaActual]
            #Caso de no estar en un extremo
            else:
                #Se define el trozo a promediar
                trozoAPromediar = self.definirTrozoFuncion(tamVentana, radio, filaActual, columnaActual, [])
                #self.__listaDeListas[filaActual][columnaActual - radio : columnaActual + radio + 1]
                #Se crea una matriz con el trozo a promediar
                trozoFuncion = Matriz(trozoAPromediar)
                #Se realiza el promedio
                promedio = trozoFuncion.calcularPromedio()
            #Se asigna el valor del resultado a la matriz de ceros
            resultado.setValor(filaActual, columnaActual, promedio)
            #Continúo con el siguiente promedio
            return self.filtrarPromediadoAux(tamVentana, resultado, filaActual, columnaActual + 1)
        #Cuando se llega al final de la fila pasa a la siguiente
        elif(filaActual < self.__filas and columnaActual == self.__columnas):
            return self.filtrarPromediadoAux(tamVentana, resultado, filaActual + 1, 0)
        #A la hora de llegar al final de la matriz retorna el resultado
        else:
            return resultado
        
    def definirTrozoFuncion(self, tamVentana, radio, filaActual, columnaActual, resultado):
        #Consigue las filas necesarias
        filasPreliminares = self.__listaDeListas[filaActual - radio : filaActual + radio + 1]
        #Hace slicing de las filas con las coulmnas necesitadas
        filasPreliminares = self.definirTrozoFuncionAux(tamVentana, radio, filasPreliminares, columnaActual, resultado, 0)
        return filasPreliminares
    
    def definirTrozoFuncionAux(self, tamVentana, radio, filas, columnaActual, resultado, indice): #indice se podria cambiar por fila actual
        if(indice < tamVentana):
            filaActual = filas[indice]
            filaActual = filaActual[columnaActual - radio : columnaActual + radio + 1]
            resultado.append(filaActual)
            self.definirTrozoFuncionAux(tamVentana, radio, filas, columnaActual, resultado, indice + 1)
        else:
            return resultado
            

    def calcularImagenIntegral(self):
        #Crea una matriz de ceros
        imagenIntegral = Matriz([], self.__filas, self.__columnas)
        #Calcula la imagen integral y la guarda en la matriz creada
        self.calcularImagenIntegralAux(self.__filas - 1, self.__columnas - 1, imagenIntegral)
        #Retorna el resultado
        return imagenIntegral
    
    
    #La va creando del último elemento al primero
    def calcularImagenIntegralAux(self, fila, columna, imagenIntegral):
        #Si se sale de la matriz, retorna 0
        if(fila < 0 or columna < 0):
            return 0;
        else:
            
            #Se suma el elemento de arriba y el de la izquierda con el valor original de la posición, y se le resta la que está a la esquina superior izquierda para compensar 
            valor = self.calcularImagenIntegralAux(fila - 1, columna, imagenIntegral) + self.calcularImagenIntegralAux(fila, columna - 1, imagenIntegral) + self.__listaDeListas[fila][columna] - self.calcularImagenIntegralAux(fila - 1, columna - 1, imagenIntegral);
            #Le asigna el valor calculado a la matriz de ceros
            imagenIntegral.setValor(fila, columna, valor);
            #??????????????????????????????? No sé por qué retorna el valor
            return valor
        
    def filtrarPromediadoLocalImagenIntegral(self, tamVentana):
        
        imagenIntegral = self.calcularImagenIntegral()
        resultado = Matriz([], self.__filas, self.__columnas)
        

    def filtrarPromediadoLocalImagenIntegralAux(self, tamVentana, resultado, filaActual, columnaActual, imagenIntegral):
        radio = tamVentana // 2;
        if(filaActual < self.__filas and columnaActual  < self.__columnas):
            #caso extremo invalido
            if(filaActual - radio < 0 or filaActual + radio > self.__filas or columnaActual - radio < 0 or columnaActual + radio > self.__columnas ):
                promedio = self.__listaDeListas[filaActual][columnaActual];
            else: #caso no extremo
                x0 = filaActual - radio - 1
                y0 = columnaActual - radio - 1
                x1 = filaActual + radio
                y1 = columnaActual  + radio
                A = (x0, y0)
                B = (x1, y0)
                C = (x0, y1)
                D = (x1, y1)
                IsigmaA = 0
                IsigmaB = 0
                IsigmaC = 0
                IsigmaD = imagenIntegral.getValor(D[0], D[1])
                if(A[0] > 0 and A[1] > 0):
                    IsigmaA = imagenIntegral.getValor(A[0], A[1])
                if(B[0] > 0 and B[1] > 0):
                    IsigmaB = imagenIntegral.getValor(B[0], B[1])
                if(C[0] > 0 and C[1] > 0):
                    IsigmaC = imagenIntegral.getValor(C[0], C[1])
                promedio = (IsigmaA  + IsigmaD - IsigmaC - IsigmaB ) / (tamVentana * tamVentana)
                resultado.setValor(filaActual, columnaActual, promedio)



principal()
