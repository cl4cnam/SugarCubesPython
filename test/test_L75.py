from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	paral:
		branch:
			diffuse 'e'
		branch:
			diffuse 'f'
			await 'e'
			await OR('e', 'f')
			print 'Hello World !'

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
