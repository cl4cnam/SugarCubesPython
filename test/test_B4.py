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

@active
class Veterinaire: pass

Brownie = Otarie()
Candie = Otarie()



expected = '''
1 :
aw !
aw !
2 :
aw !
aw !
3 :
aw !
aw !
'''
