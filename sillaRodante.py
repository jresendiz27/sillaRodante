import cgi
import urllib
#para generar los archivos json!!!
import json
#para generar un template de String
from string import Template
# [START import_ndb]
from google.appengine.ext import ndb
# [END import_ndb]

import webapp2

MAIN_PAGE = Template("""\
    <html>
        <body>
            <hr>
            $mensaje
            <hr>
            $formularioACargar
            <hr>
            DevF Team 2014
            <hr>
        </body>
    </html> 
""")
#formularios
GUARDAR_PUNTOS_CLAVE_FORM = """
    <form action="/guardarPuntoClave" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
"""
OBTENER_PUNTOS_ENTRE_AREA_FORM = """
    <form action="/obtenerPuntos" method="get">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
"""

def obtenerAreaDeBusqueda(punto1,punto2):
    #lista de los puntos cardinales
    puntosCardinales = ['norte','sur','este','oeste']
    puntosMasLejanos = {}
    puntosMasLejanos['latitudMaxima'] = 0.0
    puntosMasLejanos['longitudMaxima'] = 0.0
    puntosMasLejanos['latitudMinima'] = 0.0
    puntosMasLejanos['longitudMinima'] = 0.0
    #Se considera una diferencia de 0.0001 para los rangos, Gracias a Ricardo por ayudar a determinar la ubicacion del punto
    diferencia = 0.0001
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

# [START model]
class Util:
    #Metodo Web para obtener los puntos entre cierto rango
    def obtenerPuntos(self,request):
        punto1 = Punto()
        punto2 = Punto()
        #Se obtiene la ubicacion del cliente
        latitudOrigen = float(request.get('latitudCliente'))
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
        rangos =  obtenerAreaDeBusqueda(punto1,punto2)
        #Se ejecuta la consulta con los parametros obtenidos
        puntos = PuntoClave.gql("""
                    select * from 
                        puntosClave 
                    where 
                        latitud < :latMax 
                    and 
                        latitud <:latMin 
                    and 
                        longitud < :lonMax 
                    and 
                        longitud > :lonMin 
                    order by 
                        valoracion desc
                        """,
                        latMax = rangos['latitudMaxima'],
                        latMin = rangos['latitudMinima'],
                        lonMax = rangos['longitudMaxima'],
                        lonMin = rangos['longitudMinima']).all()
        return puntos
class Punto:
    def __init__(self):
        self.latitud = 0.0
        self.longitud = 0.0

class PuntoClave(ndb.Model):
    """Modelo de la tabla en la base de datos"""
    latitud = ndb.FloatProperty()
    longitud = ndb.FloatProperty()
    valoracion = ndb.FloatProperty()
# [END model]

# [START pagina principal] esta es la que se muestra por el momento como parte del formulario
class GuardarPuntosClavePage(webapp2.RequestHandler):
    def get(self):  
        mensajeExito = 'Guardaro Correctamente!'
        try:
            puntoAGuardar = PuntoClave()
            puntoAGuardar.latitud = float(self.request.get('latitud'))
            puntoAGuardar.longitud = float(self.request.get('longitud'))
            puntoAGuardar.valoracion = int(self.request.get('valoracion'))
            puntoAGuardar.put()
            self.response.write(MAIN_PAGE.substitute(mensaje=mensajeExito,formularioACargar=GUARDAR_PUNTOS_CLAVE_FORM))
        except Exception as e:
           self.response.write(MAIN_PAGE.substitute(mensaje=e,formularioACargar=GUARDAR_PUNTOS_CLAVE_FORM))

class MostrarPuntosClavePage(webapp2.RequestHandler):
    utileria = Util()
    def get(self):
        listadoDePuntos = utileria.obtenerPuntos(self.request)
        jsonAMostrar = json.dumps(listadoDePuntos, sort_keys=True,
                 indent=4, separators=(',', ': '))
        self.response.write(jsonAMostrar)
        #self.redirect('/?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication([
    ('/guardarPuntosClave', GuardarPuntosClavePage),
    ('/mostrarPuntosClave', MostrarPuntosClavePage),
], debug=True)
