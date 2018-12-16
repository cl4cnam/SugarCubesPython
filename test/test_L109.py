from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	paral:
		killS 'f':
			repeat 5:
				await AND('e', 'f')
				print 'Hello World !'
		repeat 5:
			generate 'e'
			generate 'f'

expected = '''
1 :
Hello World !
2 :
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
