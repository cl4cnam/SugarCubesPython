from SugarCubesDeco import *

maxI = 3



@active
class Otarie:
	
	@actionForever
	def crie(self):
		print('aw !')

Brownie = Otarie()



expected = '''
1 :
aw !
2 :
aw !
3 :
aw !
'''
