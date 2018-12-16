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
		self.an_poids /= 10
		self.diffuseInNextInstant('maigrit', self.an_poids)

@active
class Soigneur:
	
	@actionForever
	def ditBonjour(self):
		print('Bonjour !')
	
	@on('imc')
	def sAlarme(self, pList_lesImc):
		ln_sommeImc = 0
		for imc in pList_lesImc:
			ln_sommeImc += imc
		if ln_sommeImc/2.0 < 5: # 2 otaries
			print('oups, elles ont trop faim !')
	
	@on('maigrit')
	def sAlarme2(self, pList_lesPoids):
		ln_sommePoids = 0
		for poids in pList_lesPoids:
			ln_sommePoids += poids
		if ln_sommePoids/2.0 > 10: # 2 otaries
			print("c'est encore bon ?")

Candice = Soigneur()

Brownie = Otarie()
Candie = Otarie()



expected = '''
1 :
Bonjour !
aw !
aw !
2 :
c'est encore bon ?
Bonjour !
aw !
aw !
3 :
oups, elles ont trop faim !
Bonjour !
aw !
aw !
'''
