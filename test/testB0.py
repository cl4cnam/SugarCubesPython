from SugarCubes import *

@active
class Otarie:
	
	def __init__(self, ps_nom):
		self.as_nom = ps_nom
	
	def ditBonjour(self):
		print("Bonjour, je m'appelle " + self.as_nom)
	
	@automatic(forever)
	def crie(self):
		return [
			Print('wah'),
			Pause(),
			Action(self.ditBonjour),
			Pause(),
		]

m = Monde()
m.addActor(Otarie('Lucky'))
m.react()
m.react()
m.react()
m.react()
