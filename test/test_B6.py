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

@active
class Soigneur:
	
	@actionForever
	def ditBonjour(self):
		print('Bonjour !')
	
	@on('imc')
	def sAlarme(self, pList_lesImc):
		ln_sommeImc = 0
		for imc2 in pList_lesImc:
			ln_sommeImc += imc2
		if ln_sommeImc/2.0 < 5: # 2 otaries
			print('oups, elles ont trop faim !')

Candice = Soigneur()

Brownie = Otarie()
Candie = Otarie()



expected = '''
1 :
Bonjour !
aw !
aw !
2 :
Bonjour !
aw !
aw !
3 :
oups, elles ont trop faim !
Bonjour !
aw !
aw !
'''
