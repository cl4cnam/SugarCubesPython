from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	paral:
		repeat forever:
			killL 'f':
				repeat forever:
					await 'e'
					print 'Hello World !'
			pause
			generate 'g'
		repeat 5:
			generate 'e'

expected = '''
1 :
Hello World !
2 :
Hello World !
3 :
Hello World !
4 :
Hello World !
5 :
Hello World !
6 :
7 :
8 :
9 :
10 :
'''
