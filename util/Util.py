import logging as logger
from operator import itemgetter, attrgetter
import math
from operator import itemgetter, attrgetter

import numpy as np

from modelos.PuntoClave import PuntoClave
from util.Punto import Punto

MAX_WAYPOINTS = 4


class Util:
    # Metodo Web para obtener los puntos entre cierto rango
    # Constante que define google

    def obtenerAreaDeBusqueda(self, punto1, punto2):
        # lista de los puntos cardinales
        puntosMasLejanos = {}
        puntosMasLejanos['latitudMaxima'] = 0.0
        puntosMasLejanos['longitudMaxima'] = 0.0
        puntosMasLejanos['latitudMinima'] = 0.0
        puntosMasLejanos['longitudMinima'] = 0.0
        # Se considera una diferencia de 0.0001 para los rangos, Gracias a Ricardo por ayudar a determinar la ubicacion del punto
        diferencia = 0.0003
        #Se determina la ubicacion por una comparacio, gracias a Joaquin por ayudar a la visualizacion de los puntos en un plano x,y
        if punto1.latitud >= punto2.latitud:
            #Punto 1 arriba de punto 2
            #Se calculan el maximo y el minimo de las latitudes
            puntosMasLejanos['latitudMaxima'] = punto1.latitud + diferencia
            puntosMasLejanos['latitudMinima'] = punto2.latitud - diferencia
        else:
            #Punto 2 arriba de punto 1
            #Se calculan el maximo y el minimo de las latitudes
            puntosMasLejanos['latitudMaxima'] = punto2.latitud + diferencia
            puntosMasLejanos['latitudMinima'] = punto1.latitud - diferencia
        #
        #Se determina la ubicacion de la longitud
        #
        if punto1.longitud >= punto2.longitud:
            #Punto 1 a la derecha de punto 2
            #Se calculan el maximo y el minimo de las longitudes
            puntosMasLejanos['longitudMaxima'] = punto1.longitud + diferencia
            puntosMasLejanos['longitudMinima'] = punto2.longitud - diferencia
        else:
            #Punto 1 a la derecha de punto 2
            #Se calculan el maximo y el minimo de las longitudes
            puntosMasLejanos['longitudMaxima'] = punto2.longitud + diferencia
            puntosMasLejanos['longitudMinima'] = punto1.longitud - diferencia
        logger.error("Area de Busqueda")
        logger.error(puntosMasLejanos)
        return puntosMasLejanos

    def obtenerPuntos(self, request):
        punto1 = Punto()
        punto2 = Punto()
        puntosFiltrados = []
        puntosOrdenadosPorTipo = []
        try:
            # Se obtiene la ubicacion del cliente
            latitudOrigen = float(request.get('latitudOrigen'))
            longitudOrigen = float(request.get('longitudOrigen'))
            # se asigna la informacion al punto
            punto1.latitud = latitudOrigen
            punto1.longitud = longitudOrigen
            #Se obtiene el punto al que el cliente desea llegar
            latitudDestino = float(request.get('latitudDestino'))
            longitudDestino = float(request.get('longitudDestino'))
            #se asigna la informacion al punto
            punto2.latitud = latitudDestino
            punto2.longitud = longitudDestino
            #Se calculan las latitudes maximas y minimas llamando al metodo generado previamente
            rangos = self.obtenerAreaDeBusqueda(punto1, punto2)
            #Se ejecuta la consulta con los parametros obtenidos, primero se filtra la latitud
            puntosFiltro1 = PuntoClave.query(PuntoClave.latitud <= rangos['latitudMaxima'],
                                             PuntoClave.latitud >= rangos['latitudMinima']).fetch(100)
            #Se aplica un segundo filtro, limitantes de Datastore (NoSQL) por razones de indices.
            puntosFiltrados = filter(
                lambda punto: punto.longitud <= rangos['longitudMaxima'] and punto.longitud >= rangos['longitudMinima'],
                puntosFiltro1)
            puntosOrdenadosPorTipo = sorted(puntosFiltrados, key=attrgetter('tipo', 'valoracion'), reverse=True)
            return puntosOrdenadosPorTipo
        except Exception as e:
            logger.error("No se pudieron obtener los puntos")
            logger.error(e)
        return puntosOrdenadosPorTipo

    def lecturaProperties(self):
        valores = dict(line.strip().split('=') for line in open('passwords.properties'))
        return valores

    def esPuntoSemejante(self, puntoAComparar):
        diferencia = 0.0001
        # Se generan las diferencias
        latitudMaxima = puntoAComparar.latitud + diferencia
        latitudMinima = puntoAComparar.latitud - diferencia
        longitudMaxima = puntoAComparar.longitud + diferencia
        longitudMinima = puntoAComparar.longitud - diferencia
        #Se hace la consulta 1
        listaPuntosFiltro1 = PuntoClave.query()
        listaPuntosFiltro2 = listaPuntosFiltro1.filter(PuntoClave.latitud <= latitudMaxima,
                                                       PuntoClave.latitud >= latitudMinima).fetch(100)
        #listaPuntosFiltro3 = listaPuntosFiltro2.filter(PuntoClave.longitud<=longitudMaxima,PuntoClave.longitud>=longitudMinima).fetch(1)
        listaPuntosFiltro3 = filter(lambda punto: punto.longitud >= longitudMaxima and punto.longitud <= longitudMinima,
                                    listaPuntosFiltro2)
        if len(listaPuntosFiltro3):
            return listaPuntosFiltro3[0]
        else:
            return False

    def distanciaEntrePuntos(self, punto1, punto2):
        #
        lat1 = punto1.latitud
        lon1 = punto1.longitud
        #
        lat2 = punto2.latitud
        lon2 = punto2.longitud
        R = 6371
        a = 0.5 - math.cos((lat2 - lat1) * math.pi / 180) / 2 + math.cos(lat1 * math.pi / 180) * math.cos(
            lat2 * math.pi / 180) * (1 - math.cos((lon2 - lon1) * math.pi / 180)) / 2
        return R * 2 * math.asin(math.sqrt(a))

    def expandirPunto(self, punto):
        puntoExpandido = punto
        puntoExpandido.latitud += 0.005
        puntoExpandido.longitud += 0.005
        return puntoExpandido

    def calcularDistanciaOrigen_Destino(self, punto, origen, destino):
        punto.distanciaOrigen = self.distanciaEntrePuntos(punto, origen)
        punto.distanciaDestino = self.distanciaEntrePuntos(punto, destino)
        return punto

    def filtroDistancias(self, puntosAFiltrar, distanciaMaxima):
        #se calcula el entero de la distancia
        distanciaEntera = int(math.ceil(distanciaMaxima * 10))
        #se genera la matriz que almacenara los primeros puntos a filtrar
        matrizAFiltrar = np.zeros((distanciaEntera, distanciaEntera))
        for punto in puntosAFiltrar:
            distanciaRespectoOrigen = int(punto.distanciaOrigen * 10)
            distanciaRespectoDestino = int(punto.distanciaDestino * 10)
            if (
            matrizAFiltrar[distanciaRespectoOrigen][distanciaRespectoDestino]).distanciaOrigen >= punto.distanciaOrigen:
                matrizAFiltrar[distanciaRespectoOrigen][distanciaRespectoDestino] = punto
        #Se obtienen todos los puntos
        listaFiltrada = []
        for indiceX in range(0, distanciaEntera):
            for indiceY in range(0, distanciaEntera):
                if matrizAFiltrar[indiceX][indiceY]:
                    listaFiltrada.append(matrizAFiltrar[indiceX][indiceY])
        return listaFiltrada

    def filtroExpansion(self, puntosAFiltrar, diferenciaExpansion, distanciaTotal):
        numeroPuntos = len(puntosAFiltrar)
        #se genera la matriz que almacenara los primeros puntos a filtrar
        matrizAFiltrar = np.zeros((puntosAFiltrar, puntosAFiltrar))

    #Eliminacion a lo tonto!!!
    def limpiarPuntos(self, listaDePuntos):
        if len(listaDePuntos) <= MAX_WAYPOINTS:
            #No necesita ser limpiada
            return listaDePuntos
        else:
            listaParcial = []
            if (len(listaDePuntos) % 2) == 0:
                listaParcial = self.recortarPares(listaDePuntos)
            else:
                listaParcial = self.recortarPares(listaDePuntos)
        return self.limpiarPuntos(listaParcial)

    def obtenerMasCercanos(self, listaDePuntos, origen, destino):
        pass

    def recortarPares(self, listaALimpiar):
        listaSinPares = []
        if len(listaALimpiar) >= MAX_WAYPOINTS:
            for indice in range(0, len(listaALimpiar)):
                if not (indice % 2):
                    listaSinPares.append(listaALimpiar[indice])
            return listaSinPares
        else:
            return listaALimpiar

    def recortarImpares(self, listaALimpiar):
        listaSinImpares = []
        if len(listaALimpiar) >= MAX_WAYPOINTS:
            for indice in range(0, len(listaALimpiar)):
                if indice % 2:
                    listaSinImpares.append(listaALimpiar[indice])
            return listaSinImpares
        else:
            return listaALimpiar

    def distanciaEuclidiana(self, puntoA, puntoB):
        return math.sqrt(
            ((puntoA.latitud - puntoB.latitud) ** 2)
            +
            ((puntoA.longitud - puntoB.longitud) ** 2))

    def porVecinosIntercalados(self, listaDePuntos, origen, destino):
        #Se obtienen todos los vecinos con las respectivas distancias
        listaPuntosConDistancias = []
        for punto in listaDePuntos:
            puntoAux = Punto()
            puntoAux.latitud = punto.latitud
            puntoAux.longitud = punto.longitud
            puntoAux.distanciaOrigen = self.distanciaEuclidiana(puntoAux, origen)
            puntoAux.distanciaDestino = self.distanciaEuclidiana(puntoAux, destino)
            listaPuntosConDistancias.append(puntoAux)
        listaOrdenadaOrigen = sorted(listaPuntosConDistancias, key=attrgetter('distanciaOrigen'), reverse=True)
        listaOrdenadaDestino = sorted(listaPuntosConDistancias, key=attrgetter('distanciaDestino'), reverse=True)
        listaFinal = []
        valorPrevio = 0
        while True:
            listaOrdenadaOrigen = self.recortarPares(listaOrdenadaOrigen)
            listaOrdenadaDestino = self.recortarPares(listaOrdenadaDestino)
            listaFinal = list((set(listaOrdenadaOrigen + listaOrdenadaDestino)))
            valorPrevio = 0
            if (len(listaFinal) <= MAX_WAYPOINTS) or (len(listaFinal) is valorPrevio):
                break
            else:
                valorPrevio = len(listaFinal)
            logger.error(len(listaFinal))
        logger.info("--------------------------------")
        logger.info("--------------------------------")
        logger.info("--------------------------------")
        logger.info("--------------------------------")
        for elemento in listaFinal:
            logger.info(elemento)
        logger.info("--------------------------------")
        logger.info("--------------------------------")
        logger.info("--------------------------------")
        #Se eliminan los que son de tipo 1 (rojo)
        listaFinal = filter(lambda punto: punto.tipo <> 1,listaFinal)
        logger.warn("--------------------PUNTOS FILTRADOS POR TIPO--------------------")
        for elemento in listaFinal:
            logger.info(elemento)
        logger.warn("--------------------PUNTOS FILTRADOS POR TIPO--------------------")
        #Se procede a ordenar por el tipo y luego por el valor del mismo
        return listaFinal
    def imprimirLista(lista):
        for objeto in lista:
            logger.warn(objeto)