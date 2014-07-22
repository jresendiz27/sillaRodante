import logging as logger

from util.Punto import Punto

# se utilizara el fetch de google!
import urllib
from google.appengine.api import urlfetch


class MapTool:
    def conectarConServicio(self):
        pass

    def obtenerRutasOptimasEntrePuntos(self, origen, destino, puntosAConsiderar):
        url = "https://maps.googleapis.com/maps/api/directions/json?"
        form_fields = {
            "origin": str(origen),
            "destination": str(destino),
            "sensor": "false",
            "alternatives": "true",
            #"optimize":"true", #para evitar que las rutas sean medio weird ...
            "mode": "walking"  #Para evitar rutas que tengan que ver con automoviles
        }
        #Se generan los puntos a pasar en forma de cadena
        if len(puntosAConsiderar):
            waypointsCadena = "optimize:true|".join([str(punto) for punto in puntosAConsiderar])
            form_fields['waypoints'] = waypointsCadena
        #Se prepara la peticion
        #El diccionario de campos se limpia de caracteres erroneos
        form_data = urllib.urlencode(form_fields)
        #logger.info(form_data)
        #Se Obtiene la respuesta del servicio de google!
        logger.info(url + form_data)
        result = urlfetch.fetch(url=(url + form_data),
                                method=urlfetch.GET,
                                headers={'Content-Type': 'text/plain; charset=utf-8'})
        #logger.info("-"*70)
        #logger.info(result.content)
        #logger.info("-"*70)
        return result.content

    def codificarPunto(self, punto):
        pass

    def obtenerPuntos(self, request):
        #se generan instancias de los puntos
        logger.debug("------->")
        logger.debug(request)
        puntoOrigen = None
        puntoDestino = None
        try:
            puntoOrigen = Punto()
            puntoDestino = Punto()
            #Se asignan los valores de request
            #Origen
            puntoOrigen.latitud = float(request.get('latitudOrigen'))
            puntoOrigen.longitud = float(request.get('longitudOrigen'))
            #Destino
            puntoDestino.latitud = float(request.get('latitudDestino'))
            puntoDestino.longitud = float(request.get('longitudDestino'))
        except Exception as e:
            logger.error("No se pudieron convertir los parametros de la peticion a puntos geograficos.")
            logger.error(e)
        #Se imprime el error en caso de existir, y se regresan los objetos
        return puntoOrigen, puntoDestino