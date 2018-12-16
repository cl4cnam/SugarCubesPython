from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	paral:
		repeat forever:
			killS 'f':
				repeat forever:
					await 'e'
					print 'Hello World !'
			pause
			generate 'g'
		repeat 5:
			generate 'e'
		repeat 3:
			pause
			generate 'f'

expected = '''
1 :
Hello World !
2 :
Hello World !
3 :
4 :
5 :
Hello World !
6 :
7 :
8 :
9 :
10 :
'''
