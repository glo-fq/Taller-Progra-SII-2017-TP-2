from datetime import datetime
import os
import numpy
import time
import sys
from scipy import misc
sys.setrecursionlimit(10**9)    

def principal():
    
    
    #matrizImagen = misc.imread("C:/Users/Gloriana/Documents/TEC/Semestre II/Progra/TP2/20_20.png", 1)
    #matrizImagen = Matriz(matrizImagen)
    #respuesta = matrizImagen.filtrarPromediadoLocalImagenIntegral(3)
    #print(respuesta)
    #misc.imsave("prueba12.bmp", respuesta)
    #menu = Menu(sys.argv)
    
    #matrizA = Matriz([[25, 144, 1, 9, 4], [25, 4, 9, 1, 16], [9, 1, 4, 9, 1], [16, 9, 4, 1, 9], [1, 25, 36, 25, 9]])
    #answer = matrizA.filtrarPromediadoLocalImagenIntegral(3)
    #print(answer)

"""
    OTRAS PRUEBAS

    #Así se recibe información de la consola
    
    
    #Ejemplo matriz del enunciado
    #matrizA = Matriz([[25, 144, 1, 9, 4], [25, 4, 9, 1, 16], [9, 1, 4, 9, 1], [16, 9, 4, 1, 9], [1, 25, 36, 25, 9]])
    
    #Ejemplo de matriz de una sola fila
    #matrizB = Matriz([[0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0]])
    
    #Aquí hace el método por imagen integral
    #f = matrizA.filtrarPromediadoLocalImagenIntegral(3)
    #print("f: ", f)
    #misc.imsave("prueba1.bmp", f)
    
    #Aquí se usa el método de promediar
    #conv = matrizA.filtrarPromediado(3)
    #print("conv: ", conv)
		
"""



class Menu:
    """
    Constructor del menú, el cual define todos los detalles para la ejecución del programa
    @param argumentos, los argumentos dados por el usuario en la consola
    """
    def __init__(self, argumentos):
        
        #Define el archivo que se va a analizar
        self.__archivoEntrada = self.encontrarImagenEntrada()
        #Encuentra el método que se especificó
        self.__metodo = self.definirMetodo(argumentos)
        #Define el ancho de ventana
        self.__anchoVentana = self.definirAnchoVentana(argumentos)
        #Defune el nombre que tendrá el archivo 
        self.__nombreSalida = self.definirNombreArchivoSalida(argumentos, datetime.now())
        resultado = self.aplicarFiltro()
        self.guardarImagenResultado(resultado)
        
    """
    El usuario define la ruta y nombre de la imagen a convertir y se lee esta imagen como matriz
    return misc.imread, la cual abre la imagen en escala de grises
    """
    def encontrarImagenEntrada(self):
        rutaImagenEntrada = input("Por favor escriba la ruta del archivo al que desea aplicar el filtro: ")
        nombreArchivoEntrada = input("Escriba el nombre del archivo a leer: ")
        #Junta la ruta con el nombre del archivo que se quiere abrir
        rutaCompleta = os.path.join(rutaImagenEntrada, nombreArchivoEntrada)
        #Retorna la matriz de la imagen en escala de grises
        return  misc.imread(rutaCompleta, 1)
        
    """
    Define el método que se va a utilizar para eliminar el ruido, sea por imágenes integrales tanto como promediado
    @param argumentos, los argumentos proporcionados por el usuario para la ejecución
    return metodoAUtilizar, el método que se definió se va a usar
    """
    def definirMetodo(self, argumentos):
        #Se retorna el valor que se indique luego del argumento "-m"
        metodoAUtilizar = argumentos[argumentos.index("-m") + 1]
        return metodoAUtilizar
    
    """
    Define el ancho de la ventana según lo que el usuario proporcionó
    @param argumentos, los argumentos dados por el usuario cuando se llamó al programa
    return ancho, el ancho definido
    """
    def definirAnchoVentana(self, argumentos):
        ancho = argumentos[argumentos.index("-v") + 1]
        ancho = int(ancho)
        #Si encuentra el siguiente parámetro, esto indica que no se especificó el ancho de ventana
        if (ancho == "-m"):
            ancho = 3
        return ancho

    """
    Basado en la información que provee el usuario, se define el archivo de salida
    @argumentos, son los argumentos dados en la consola por el usuario
    @instante, el momento de la creación de la imagen de resultado
    return nombreArchivoSalida, el nombre que se designó para la imagen de resultado
    """
    def definirNombreArchivoSalida(self, argumentos, instante):
        #Si el usuario definió un nombre de archivo de salida, se designa este como tal
        try:
            nombreArchivo = argumentos[argumentos.index("-o") + 1]
            #Si el argumento después de -o no es donde se define el ancho de la ventana, es un nombre válido
            if (nombreArchivo != "-v"):
                return nombreArchivo
            else:
                return ("%s_%s_%s_%s_%s_%s.bmp" % (instante.day, instante.month, instante.year, instante.hour, instante.minute, instante.second))
        except:
            return ("%s_%s_%s_%s_%s_%s.bmp" % (instante.day, instante.month, instante.year, instante.hour, instante.minute, instante.second))
        
    """
    Aplica el filtro especificado por el usuario
    """
    def aplicarFiltro(self):
        matriz = Matriz(self.__archivoEntrada)
        #Si es por imágenes integrales, se llama a este método
        if(self.__metodo == "ii"):
            return matriz.filtrarPromediadoLocalImagenIntegral(self.__anchoVentana)
        #Si es por promediado, se llama a filtrar promediado
        elif(self.__metodo == "conv"):
            return matriz.filtrarPromediado(self.__anchoVentana)

    
    """
    Guarda el resultado generado en una imagen. Se pide al usuario la ruta en la que se guardará la imagen.
    @param resultado, es la matriz de resultado tras haber realizado uno de los métodos de filtrado
    """
    def guardarImagenResultado(self, resultado):
        rutaArchivoSalida = input("Escriba la ruta donde se desea guardar la imagen de resultado.")
        #A la ruta se le agrega el nombre del archivo
        rutaCompleta = os.path.join(rutaArchivoSalida, self.__nombreSalida)
        #Se salva la matriz que resultó
        misc.imsave(rutaCompleta, resultado)            
            
            
    
class MatrizCeros:
    """
    Construye una matriz de ceros con la cantidad de filas y columnas especificadas
    """
    def __init__(self, numFilas, numColumnas):
        self.__listaDeListas = numpy.zeros((numFilas, numColumnas))
        self.__filas = numFilas
        self.__columnas = numColumnas
        print("Se ha creado una matriz de ceros.")
        print(self.__listaDeListas)

class Matriz:
	
    """
    Se construye la matriz
    @param listaDeListas, la matriz recibida en forma de lista de listas
    @param numFilas, cantidad de filas de la matriz
    @param numColumnas, cantidad de columnas de la matriz
    @return la instancia de la matriz
    """
    def __init__(self, listaDeListas):
        self.__listaDeListas = numpy.array(listaDeListas, dtype=float)
        self.__filas = len(listaDeListas)
        self.__columnas = len(listaDeListas[0])
        print("Se creó una matriz convencional.")
        print(self.__listaDeListas)           


    """
    Define la lista de listas de un objeto dado
    @param listaDeListas, la lista de listas recibida
    """
    def setListaDeListas(self, listaDeListas):
    	self.__listaDeListas = listaDeListas
    	self.__filas = len(listaDeListas)
    	self.__columnas = len(listaDeListas[0])

    """
    Retorna la matriz que se está consultando
    """
    def getListaDeListas(self):
    	return self.__listaDeListas

    """
    Define el valor de un lugar de la matriz
    @param fila, la fila que será modificada
    @param columna, la columna que se va a cambiar
    @param valor, el valor que se va a designar
    """
    def setValor(self, fila, columna, valor):
    	self.__listaDeListas[fila, columna] = valor
        

    """
    Retorna el valor que se está pidiendo
    @param fila, la fila que se consulta
    @param columna, la columna que se consulta
    return elemento, el elemento que se encuentra en la posición dada
    """
    def getValor(self, fila, columna):
    	return self.__listaDeListas[fila, columna]

    """
    La conversión para que cuando imprimo la matriz, se imprima como hilera
    """
    def __str__(self):
        hilera = str(self.__listaDeListas)
        #Para realizar pruebas hay una hilera que además de enseñar la matriz, imprime la cantidad de filas y columnas que esta posee
        hileraConInformacion = "Matriz: " + str(self.__listaDeListas) + "\n Numero de filas: " + str(self.__filas) + "\n Numero de columnas: " + str(self.__columnas)
        return hilera

    """
    Calcula el promedio de una matriz
    """
    def calcularPromedio(self):
        return self.calcularPromedioAux(0, 0)

    """
    Realiza el cálculo del promediado con cada elemento de la matriz recibida
    @param filaActual, es la fila que se está analizando
    @param columnaActual, la columna que se está analizando
    return promedio, el promedio de los elementos analizados
    """
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

    """
    @param tamVentana, el tamaño de la ventana de promediado
    """
    def filtrarPromediado(self, tamVentana):
        #Crea una matriz de ceros
        resultado = MatrizCeros(self.__filas, self.__columnas)
        #Se obtienen las listas
        resultado = self.__listaDeListas
        #Se llama a la función auxiliar
        resultado = self.filtrarPromediadoAux(tamVentana, resultado, 1, 1)
        print(resultado)
        return resultado

    """
    @param tamVentana, el tamaño de la ventana de promediado
    @param resultado, la matriz donde se va guardando el resultado
    @param batchFilaActual, el trozo de fila al que se le va a aplicar el promediado
    @param batchColActual, el trozo de columna al que se le va a aplicar el promediado
    return resultado, la matriz promediada
    """
    def filtrarPromediadoAux(self, tamVentana, resultado, batchFilaActual, batchColActual): #Iniciar batch en 1
        #Se cuentan cuántas veces puedo realizar un promediado con las 20 columnas completas
        batchesColumnaCompletos = self.__columnas // 20
        #Se cuentan cuántos elementos sobran. Estos se agregarán al ultimo trozo de matriz que se promediará
        batchesColumnaResiduo = self.__columnas % 20
        
        #Cuenta cuántas veces se puede hacer promediado de las 20 filas completas
        batchesFilaCompletos = self.__filas // 20
        #Se calcula cuántas filas sobran; se agregarán al último batch que se promedia
        batchesFilaResiduo = self.__filas % 20
        
        #Si no ha llegado al último batch de columnas y está recorriendo las filas:
        if(batchColActual < batchesColumnaCompletos and batchFilaActual <= batchesFilaCompletos):
            #Se definre el intervalo de columnas a promediar
            #Por ejemplo: El batch 1 será del 0 al 19, el batch 2 del 20 al 39, y así
            if(batchColActual < batchesColumnaCompletos):
                columnaInicial = (batchColActual - 1) * 20
                columnaFinal = (batchColActual * 20) - 1
             
            #Se define 
            if(batchFilaActual < batchesFilaCompletos):
                filaInicial = (batchFilaActual - 1) * 20
                filaFinal = (batchFilaActual * 20) - 1
            
            #Si ya llegó al último batch de filas, a las filas se les agrega el trozo extra
            else:
                filaInicial = batchesFilaCompletos * 20
                filaFinal = (batchFilaActual * 20) - 1 + batchesFilaResiduo
        
            #Se recorren las filas y columnas correspondientes para obtener el resultado
            self.filtrarPromediadoRecorriendoFilasAux(tamVentana, resultado, filaInicial, columnaInicial, filaFinal, columnaFinal, columnaInicial)
            self.filtrarPromediadoRecorriendoColumnasAux(tamVentana, resultado, filaInicial, columnaInicial, filaFinal, columnaFinal, columnaInicial)
        
            #Sigue con el siguiente batch de columnas
            return self.filtrarPromediadoAux(tamVentana, resultado, batchFilaActual, batchColActual + 1)
    
        #Si está en el último batch de columnas y todavía está recorriendo las filas:
        elif(batchColActual == batchesColumnaCompletos and batchFilaActual <= batchesFilaCompletos):
            columnaInicial = batchesColumnaCompletos * 20
            columnaFinal = (batchColActual * 20) - 1 + batchesColumnaResiduo
            
            #En caso de que no se haya llegado al último batch de filas, se define el intervalo a promediar
            if(batchFilaActual < batchesFilaCompletos):
                filaInicial = (batchFilaActual - 1) * 20
                filaFinal = (batchFilaActual * 20) - 1
            #Si está en el último batch de filas, se agrega el trozo extra para promediar el final
            else:
                filaInicial = batchesFilaCompletos * 20
                filaFinal = (batchFilaActual * 20) - 1 + batchesFilaResiduo
            
            
            #Se promedian las filas y columnas correspndientes
            self.filtrarPromediadoRecorriendoFilasAux(tamVentana, resultado, filaInicial, columnaInicial, filaFinal, columnaFinal, columnaInicial)
            self.filtrarPromediadoRecorriendoColumnasAux(tamVentana, resultado, filaInicial, columnaInicial, filaFinal, columnaFinal, columnaInicial)
            
            #Recorre la siguiente fila y reinicia los batches de columnas
            return self.filtrarPromediadoAux(tamVentana, resultado, batchFilaActual + 1, 1)
        
        #Si ya terminó de promediar todos los batches, se devuelve el resultado
        else:
            return resultado
            
            
        
    """
    Se realiza un promediado inicial recorriendo nada más las filas
    @param tamVentana, el tamaño de la ventana de promediado
    @param resultado, la matriz donde se va guardando el resultado
    @param filaActual, la fila actual que se está recorriendo. Se inicializa en la fila inicial del batch
    @param columnaActual, la columna que se está recorriendo. Se inicializa en la columna inicial del batch
    @param filaFinal, es la última fila que hay que recorrer antes de retornar el resultado
    @param columnaFinal, la última columna que se recorre antes de dar el resultado
    @param columnaInicial, la columna con la que se inició a promediar; se usa de referencia para resetear las columnas cada vez que se recorre una nueva fila
    return resultado, el promedio de las filas designadas 
    """
    #Paso 1: Recorrer cada fila y hacer el promedio con el intervalo del ancho de ventana especificado
    def filtrarPromediadoRecorriendoFilasAux(self, tamVentana, resultado, filaActual, columnaActual, filaFinal, columnaFinal, columnaInicial):
        #El radio se saca a partir del tam. de ventana
        radio = tamVentana // 2
        #print("Fila: ", filaActual, " Columna: ", columnaActual)
        #Cuando no se ha llegado al final
        if(filaActual <= filaFinal and columnaActual <= columnaFinal):
            #Caso de estar en un extremo: Se toma el valor original que tenía el pixel
            if((columnaActual - radio < 0) or (columnaActual + radio >= self.__columnas)):
                promedio = self.__listaDeListas[filaActual, columnaActual]
            #Caso de no estar en un extremo
            else:
                #Se define el trozo a promediar
                trozoAPromediar = self.__listaDeListas[filaActual, columnaActual - radio : columnaActual + radio + 1]
                #Se crea una matriz con el trozo a promediar
                trozoFuncion = Matriz([trozoAPromediar])
                #Se realiza el promedio
                promedio = trozoFuncion.calcularPromedio()
                print(promedio)
            #Se asigna el valor del resultado a la matriz de ceros
            resultado[filaActual, columnaActual] = promedio
            #Continúo con el siguiente promedio
            return self.filtrarPromediadoRecorriendoFilasAux(tamVentana, resultado, filaActual, columnaActual + 1, filaFinal, columnaFinal, columnaInicial)
        #Cuando se llega al final de la fila pasa a la siguiente
        elif(filaActual <= filaFinal and columnaActual > columnaFinal):
            return self.filtrarPromediadoRecorriendoFilasAux(tamVentana, resultado, filaActual + 1, columnaInicial, filaFinal, columnaFinal, columnaInicial)
        #A la hora de llegar al final de la matriz retorna el resultado
        else:
            return resultado
        
    """
    Similar a la función anterior, esta función toma los promediados que se consiguieron tras recorrer las filas y los promedia para dar el resultado final del pixel
    @param tamVentana, el tamaño de la ventana de promediado
    @param resultado, la matriz donde se va guardando el resultado
    @param filaActual, la fila actual que se está recorriendo. Se inicializa en la fila inicial del batch
    @param columnaActual, la columna que se está recorriendo. Se inicializa en la columna inicial del batch
    @param filaFinal, es la última fila que hay que recorrer antes de retornar el resultado
    @param columnaFinal, la última columna que se recorre antes de dar el resultado
    @param columnaInicial, la columna con la que se inició a promediar; se usa de referencia para resetear las columnas cada vez que se recorre una nueva fila
    return resultado, el promedio de las filas designadas 
    """
    def filtrarPromediadoRecorriendoColumnasAux(self, tamVentana, resultado, filaActual, columnaActual, filaFinal, columnaFinal, columnaInicial):
        #El radio se saca a partir del tam. de ventana
        radio = tamVentana // 2
        #Cuando no se ha llegado al final
        if(filaActual <= filaFinal and columnaActual <= columnaFinal):
            #Caso de estar en un extremo: Se toma el valor original que tenía el pixel
            if((filaActual - radio < 0) or (filaActual + radio >= self.__filas)):
                promedio = self.__listaDeListas[filaActual, columnaActual]
            #Caso de no estar en un extremo
            else:
                #Se define el trozo a promediar
                trozoAPromediar = self.__listaDeListas[filaActual - radio : filaActual + radio + 1, columnaActual]
                #Se crea una matriz con el trozo a promediar
                trozoFuncion = Matriz([trozoAPromediar])
                #Se realiza el promedio
                promedio = trozoFuncion.calcularPromedio()
                print(promedio)
            #Se asigna el valor del resultado a la matriz de ceros
            resultado[filaActual, columnaActual] = promedio
            #Continúo con el siguiente promedio
            return self.filtrarPromediadoRecorriendoColumnasAux(tamVentana, resultado, filaActual, columnaActual + 1, filaFinal, columnaFinal, columnaInicial)
        #Cuando se llega al final de la fila pasa a la siguiente
        elif(filaActual <= filaFinal and columnaActual > columnaFinal):
            return self.filtrarPromediadoRecorriendoColumnasAux(tamVentana, resultado, filaActual + 1, columnaInicial, filaFinal, columnaFinal, columnaInicial)
        #A la hora de llegar al final de la matriz retorna el resultado
        else:
            return resultado
        
        

    def calcularImagenIntegral(self):
        #Crea una matriz de ceros
        imagenIntegral = MatrizCeros(self.__filas, self.__columnas)
        imagenIntegral = self.__listaDeListas
        #Calcula la imagen integral y la guarda en la matriz creada
        self.calcularImagenIntegralAux(self.__filas - 1, self.__columnas - 1, imagenIntegral)
        #Retorna el resultado
        return imagenIntegral
    
    
    #La va creando del último elemento al primero
    def calcularImagenIntegralAux(self, fila, columna, imagenIntegral):
        #Si se sale de la matriz, retorna 0
        if(fila < 0 or columna < 0):
            return 0
        else:
            
            #Se suma el elemento de arriba y el de la izquierda con el valor original de la posición, y se le resta la que está a la esquina superior izquierda para compensar 
            valor = self.calcularImagenIntegralAux(fila - 1, columna, imagenIntegral) + self.calcularImagenIntegralAux(fila, columna - 1, imagenIntegral) + self.__listaDeListas[fila][columna] - self.calcularImagenIntegralAux(fila - 1, columna - 1, imagenIntegral)
            #Le asigna el valor calculado a la matriz de ceros
            imagenIntegral[fila, columna] = valor
            
            return valor
        
    def filtrarPromediadoLocalImagenIntegral(self, tamVentana):
        
        imagenIntegral = self.calcularImagenIntegral()
        resultado = MatrizCeros(self.__filas, self.__columnas)
        resultado = self.__listaDeListas
        
        return self.filtrarPromediadoLocalImagenIntegralAux(tamVentana, resultado, 0, 0, imagenIntegral)
        

    def filtrarPromediadoLocalImagenIntegralAux(self, tamVentana, resultado, filaActual, columnaActual, imagenIntegral):
        radio = tamVentana // 2;
        if(filaActual < self.__filas and columnaActual  < self.__columnas):
            #Caso extremo inválido (se le asigna el valor original):
            if(filaActual - radio < 0 or filaActual + radio >= self.__filas or columnaActual - radio < 0 or columnaActual + radio >= self.__columnas ):
                promedio = self.__listaDeListas[filaActual][columnaActual]                
           
            else: #Caso no extremo (se realiza el la suma y resta de imágenes integrales):

                print("IMAGEN INTEGRAL 2")
                print(imagenIntegral)
                
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
                IsigmaD = imagenIntegral[D[0], D[1]]
                if(A[0] >= 0 and A[1] >= 0):
                    IsigmaA = imagenIntegral[A[0], A[1]]
                if(B[0] >= 0 and B[1] >= 0):
                    IsigmaB = imagenIntegral[B[0], B[1]]
                if(C[0] >= 0 and C[1] >= 0):
                    IsigmaC = imagenIntegral[C[0], C[1]]
                promedio = (IsigmaA  + IsigmaD - IsigmaC - IsigmaB ) / (tamVentana * tamVentana);
            
            #Se asigna el valor promedio calculado según los 2 casos
            resultado[filaActual, columnaActual] = promedio
            #Sigue con la siguiente columna
            return self.filtrarPromediadoLocalImagenIntegralAux(tamVentana, resultado, filaActual, columnaActual + 1, imagenIntegral)         
        
        #Si llega a la última columna de la fila, se continúa con la siguiente fila
        elif(filaActual < self.__filas and columnaActual == self.__columnas):
            return self.filtrarPromediadoLocalImagenIntegralAux(tamVentana, resultado, filaActual + 1, 0, imagenIntegral)
        
        #Una vez recorrida toda la matriz, se retorna el resultado
        else:
            return resultado



principal()
