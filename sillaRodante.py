import cgi
import urllib
#para generar los archivos json!!!
import json
#para generar un template de String
from string import Template
from google.appengine.ext import ndb

import webapp2

MAIN_PAGE = Template("""\
    <html>
        <body>
            <hr>
            Mensaje del Sistema : $mensaje
            <hr>
            <h2>Formulario de carga </h2>
            $formularioACargar
            <hr>
            <h2>Formulario de consulta </h2>
            $formularioConsulta
            DevF Team 2014
            <hr>
        </body>
    </html> 
""")
#formularios
GUARDAR_PUNTOS_CLAVE_FORM = """
    <form action="/test" method="post">
      <p>
      latitud <input type="text" name="latitud">
      </p>
      <p>
      longitud <input type="text" name="longitud">
      </p>
      valoracion <input type="text" name="valoracion">
      <p>
      <input type="submit" value="guardar">
      </p>
    </form>
"""
OBTENER_PUNTOS_ENTRE_AREA_FORM = """
    <form action="/obtenerPuntos" method="post" target="respuesta">
      <p>
      latitud Origen <input type="text" name="latitudOrigen">
      </p>
      <p>
      longitud Origen<input type="text" name="longitudOrigen">
      </p>
      latitudDestino <input type="text" name="latitudDestino">
      <p>
      </p>
      longitudDestino <input type="text" name="longitudDestino">
      <p>
      <input type="submit" value="Obtener">
      </p>
    </form>
    <iframe id="respuesta" name="respuesta" width="100%" height="100%"></iframe>
"""
class Util:
    #Metodo Web para obtener los puntos entre cierto rango
    def obtenerAreaDeBusqueda(self,punto1,punto2):
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
        return puntosMasLejanos

    def obtenerPuntos(self,request):
        punto1 = Punto()
        punto2 = Punto()
        #Se obtiene la ubicacion del cliente
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
        rangos = self.obtenerAreaDeBusqueda(punto1,punto2)
        print "*"*60
        print "\n"
        print rangos
        print "*"*60
        print "\n"
        #Se ejecuta la consulta con los parametros obtenidos, primero se filtra la latitud
        puntosFiltro1 = PuntoClave.gql("""
                    where 
                        latitud <=:latMax 
                    and 
                        latitud >=:latMin 
                        """,
                        latMax = rangos['latitudMaxima'],
                        latMin = rangos['latitudMinima']).fetch(100)
        puntosFiltrados = []
        #Se aplica un segundo filtro, limitantes de Datastore (NoSQL) por razones de indices.
        #Se hace un fetch de ciertos puntos ya que se considera que no es necesario obtener todo.
        for punto in puntosFiltro1:
            if punto.longitud <= rangos['longitudMaxima'] and punto.longitud >= rangos['longitudMinima']:
                puntosFiltrados.append(punto)

        return puntosFiltrados
class Punto:
    def __init__(self):
        self.latitud = 0.0
        self.longitud = 0.0

class PuntoClave(ndb.Model):
    """Modelo de la tabla en la base de datos"""
    latitud = ndb.FloatProperty()
    longitud = ndb.FloatProperty()
    valoracion = ndb.FloatProperty()

class GuardarPuntosClavePage(webapp2.RequestHandler):
    def get(self):  
        print "Guardar puntos clave"
        mensajeExito = 'Guardaro Correctamente!'
        try:
            puntoAGuardar = PuntoClave()
            puntoAGuardar.latitud = float(self.request.get('latitud'))
            puntoAGuardar.longitud = float(self.request.get('longitud'))
            puntoAGuardar.valoracion = int(self.request.get('valoracion'))
            puntoAGuardar.put()
            print "Guardado!!!!"
            self.response.write(MAIN_PAGE.substitute(mensaje=mensajeExito,formularioACargar=GUARDAR_PUNTOS_CLAVE_FORM,formularioConsulta=OBTENER_PUNTOS_ENTRE_AREA_FORM))
            #self.redirect('/test')
        except Exception as e:
            self.response.write(MAIN_PAGE.substitute(mensaje=e,formularioACargar=GUARDAR_PUNTOS_CLAVE_FORM,formularioConsulta=OBTENER_PUNTOS_ENTRE_AREA_FORM))
    def post(self):
        self.get()

class MostrarPuntosClavePage(webapp2.RequestHandler):
    def get(self):
        print "OK--------------------------------------'\n"
        utileria = Util()
        listadoDePuntos = utileria.obtenerPuntos(self.request)
        jsonAMostrar = json.dumps([punto.to_dict() for punto in listadoDePuntos])
        self.response.write(jsonAMostrar)
        #self.redirect('/?' + urllib.urlencode(query_params))
    def post(self):
        self.get()

application = webapp2.WSGIApplication([
    ('/test', GuardarPuntosClavePage),
    ('/', GuardarPuntosClavePage),
    ('/obtenerPuntos', MostrarPuntosClavePage)
], debug=True)
