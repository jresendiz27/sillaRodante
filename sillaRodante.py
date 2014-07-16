# para generar los archivos json!!!
import json
# para generar un template de String
from string import Template
# Utileria
from util.Util import Util
# Modelos de la base de datos
from modelos.PuntoClave import PuntoClave
#Herramienta para el manejo de mapas
from util.MapTool import MapTool
from util.Punto import Punto
import logging as logger

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


class GuardarPuntosClavePage(webapp2.RequestHandler):
    def get(self):
        mensajeExito = 'Guardaro Correctamente!'
        try:
            puntoAGuardar = PuntoClave()
            puntoAGuardar.latitud = float(self.request.get('latitud'))
            puntoAGuardar.longitud = float(self.request.get('longitud'))
            puntoAGuardar.valoracion = int(self.request.get('valoracion'))
            puntoAGuardar.put()
            if bool(self.request.get('dev')):  #Si existe el parametro debug!, se genera la pagina web
                print("Guardado!!!!")
                self.response.write(
                    MAIN_PAGE.substitute(mensaje=mensajeExito, formularioACargar=GUARDAR_PUNTOS_CLAVE_FORM,
                                         formularioConsulta=OBTENER_PUNTOS_ENTRE_AREA_FORM))
            #significa que solo necesitan la respuesta en JSON, posiblemente en produccion
            else:
                mapaRespuesta = {'mensaje': 'Guardado Correctamente!'}
                self.response.headers['Content-Type'] = 'application/json'
                self.response.out.write(json.dumps(mapaRespuesta))

            #self.redirect('/test')
        except Exception as e:
            self.response.write(MAIN_PAGE.substitute(mensaje=e, formularioACargar=GUARDAR_PUNTOS_CLAVE_FORM,
                                                     formularioConsulta=OBTENER_PUNTOS_ENTRE_AREA_FORM))

    def post(self):
        self.get()


class MostrarPuntosClavePage(webapp2.RequestHandler):
    def get(self):
        utileria = Util()
        listadoDePuntos = utileria.obtenerPuntos(self.request)
        jsonAMostrar = json.dumps([punto.to_dict() for punto in listadoDePuntos])
        self.response.write(jsonAMostrar)

    #self.redirect('/?' + urllib.urlencode(query_params))
    def post(self):
        self.get()


class ObtenerRutasPage(webapp2.RequestHandler):
    def get(self):
        #clases de utileria
        utileria = Util()
        #clase para las herramientas de mapas
        mapTool = MapTool()
        #puntoOrigen,puntoDestino = mapTool.obtenerPuntos(self.request)
        puntoOrigen = None
        puntoDestino = None
        try:
            puntoOrigen = Punto()
            puntoDestino = Punto()
            #Se asignan los valores de request
            #Origen
            puntoOrigen.latitud = float(self.request.get('latitudOrigen'))
            puntoOrigen.longitud = float(self.request.get('longitudOrigen'))
            #Destino
            puntoDestino.latitud = float(self.request.get('latitudDestino'))
            puntoDestino.longitud = float(self.request.get('longitudDestino'))
        except Exception as e:
            logger.error("No se pudieron convertir los parametros de la peticion a puntos geograficos.")
            logger.error(e)
        #Se imprime el error en caso de existir, y se regresan los objetos
        puntosClave = utileria.obtenerPuntos(self.request)
        logger.warn(puntoOrigen)
        logger.warn(puntoDestino)
        rutasPosibles = mapTool.obtenerRutasOptimasEntrePuntos(puntoOrigen,puntoDestino,puntosClave)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(rutasPosibles)

    #Un little hack para que funcione por ambos metodos,se usara POST, por motivos de encapsulamiento de la informacion
    def post(self):
        self.get()


application = webapp2.WSGIApplication([
                                          ('/test', GuardarPuntosClavePage),
                                          ('/', GuardarPuntosClavePage),
                                          ('/obtenerPuntos', MostrarPuntosClavePage),
                                          ('/obtenerRutas',ObtenerRutasPage )
                                      ], debug=True)
