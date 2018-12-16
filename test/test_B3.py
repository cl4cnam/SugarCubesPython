from SugarCubesDeco import *

maxI = 3



@active
class Otarie:
	
	@actionForever
	def crie(self):
		print('aw !')

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
