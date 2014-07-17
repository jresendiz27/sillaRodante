from modelos.PuntoClave import PuntoClave
from util.Punto import Punto
import logging as logger

class Util:
    # Metodo Web para obtener los puntos entre cierto rango
    def obtenerAreaDeBusqueda(self, punto1, punto2):
        # lista de los puntos cardinales
        puntosMasLejanos = {}
        puntosMasLejanos['latitudMaxima'] = 0.0
        puntosMasLejanos['longitudMaxima'] = 0.0
        puntosMasLejanos['latitudMinima'] = 0.0
        puntosMasLejanos['longitudMinima'] = 0.0
        #Se considera una diferencia de 0.0001 para los rangos, Gracias a Ricardo por ayudar a determinar la ubicacion del punto
        diferencia = 0.03
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
        try:
            # Se obtiene la ubicacion del cliente
            latitudOrigen = float(request.get('latitudOrigen'))
            longitudOrigen = float(request.get('longitudOrigen'))
            #se asigna la informacion al punto
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
            puntosFiltro1 = PuntoClave.query(PuntoClave.latitud<=rangos['latitudMaxima'],PuntoClave.latitud>=rangos['latitudMinima']).fetch(100)
            #Se aplica un segundo filtro, limitantes de Datastore (NoSQL) por razones de indices.
            puntosFiltrados = filter(lambda punto: punto.longitud<=rangos['longitudMaxima'] and punto.longitud>=rangos['longitudMinima'],puntosFiltro1)
            return puntosFiltrados
        except Exception as e:
            logger.error("No se pudieron obtener los puntos")
            logger.error(e)
        return puntosFiltrados

    def lecturaProperties(self):
        valores = dict(line.strip().split('=') for line in open('passwords.properties'))
        return valores

    def esPuntoSemejante(self,puntoAComparar):
        diferencia = 0.0001
        #Se generan las diferencias
        latitudMaxima = puntoAComparar.latitud + diferencia
        latitudMinima = puntoAComparar.latitud - diferencia
        longitudMaxima = puntoAComparar.longitud + diferencia
        longitudMinima = puntoAComparar.longitud - diferencia
        #Se hace la consulta 1
        listaPuntosFiltro1 = PuntoClave.query()
        listaPuntosFiltro2 = listaPuntosFiltro1.filter(PuntoClave.latitud<=latitudMaxima,PuntoClave.latitud>=latitudMinima).fetch(10)
        #listaPuntosFiltro3 = listaPuntosFiltro2.filter(PuntoClave.longitud<=longitudMaxima,PuntoClave.longitud>=longitudMinima).fetch(1)
        listaPuntosFiltro3 =  filter(lambda punto: punto.longitud<=longitudMaxima and punto.longitud>=longitudMinima,listaPuntosFiltro2)
        print(listaPuntosFiltro3)
        print(listaPuntosFiltro3)
        print(listaPuntosFiltro3)
        if len(listaPuntosFiltro3):
            return listaPuntosFiltro3[0]
        else:
            return False