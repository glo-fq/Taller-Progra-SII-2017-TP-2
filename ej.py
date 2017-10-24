def principal():
    import numpy
    import time
    import sys
    from datetime import datetime
    tiempoInicio = time.clock() 

    matrizA = Matriz([[25, 144, 1, 9, 4], [25, 4, 9, 1, 16], [9, 1, 4, 9, 1], [16, 9, 4, 1, 9], [1, 25, 36, 25, 9]])

    #Ejemplo de clase de funcion rectángulo
    matrizB = Matriz([[0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0]])
    print(matrizB.__str__())
    f = matrizB.filtrarPromediado(3)
    print(f)
		
    #print((time.clock() - tiempoInicio) * 10 ** 3, "ms") 


def definirNombreArchivoSalida(instante):
	pass
	"""if():
	else:
		return ("%s_%s_%s_%s_%s_%s.bmp" % (instante.day, instante.month, instante.year, instante.hour, instante.minute, instante.second))"""

#class Filtro:
#%%
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

#%%
    """Inicializa una matriz de ceros"""
    def inicializarConCeros(self, numFilas, numColumnas):
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

#%%
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

#%%
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
            if(columnaActual - radio < 0 or columnaActual + radio > self.__columnas):
                promedio = self.__listaDeListas[filaActual][columnaActual]
            #Caso de no estar en un extremo
            else:
                #Se define el trozo a promediar
                trozoAPromediar = self.__listaDeListas[filaActual][columnaActual - radio : columnaActual + radio + 1]
                #Se crea una matriz con el trozo a promediar
                trozoFuncion = Matriz([trozoAPromediar])
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
            #???????????????????????????????
            return valor


#%%

principal()