class Punto:
	def __init__(self):
		self.latitud = 0.0
		self.longitud = 0.0

	def __str__(self):
		return "%s,%s" % (self.latitud, self.longitud)