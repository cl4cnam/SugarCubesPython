from SugarCubesDeco import *

maxI = 3



@active
class Otarie:
	
	def __init__(self):
		super().__init__()
		self.an_hauteur = 1.5
		self.an_poids = 200
	
	@publicVar
	def imc(self):
		return self.an_poids / self.an_hauteur ** 2
	
	@actionForever
	def crie(self):
		print('aw !')
	
	@actionForever
	def maigrit(self):
		self.an_poids /= 2

@active
class Soigneur:
	
	@actionForever
	def ditBonjour(self):
		print('Bonjour !')
	
	@on('imc')
	def sAlarme(self, pList_lesImc):
		print("Ah oui, l'imc")

Candice = Soigneur()

Brownie = Otarie()
Candie = Otarie()



expected = '''
1 :
Ah oui, l'imc
Bonjour !
aw !
aw !
2 :
Ah oui, l'imc
Bonjour !
aw !
aw !
3 :
Ah oui, l'imc
Bonjour !
aw !
aw !
'''
