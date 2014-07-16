from google.appengine.ext import ndb
from util import Punto
class PuntoClave(ndb.Model):
    """Modelo de la tabla en la base de datos"""
    latitud = ndb.FloatProperty()
    longitud = ndb.FloatProperty()
    tipo = ndb.IntegerProperty()
    #Se utilizara para actualizar los valores de la base de datos, se sacara un promedio de las valoraciones.
    valoracion = ndb.FloatProperty()
    numeroValoraciones = ndb.IntegerProperty()

    def __str__(self):
	    return "%s,%s" % (self.latitud,self.longitud)