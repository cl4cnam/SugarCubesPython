from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	pause forever
	await 'e'
	diffuse 'e'
	print 'Hello World !'

expected = '''
1 :
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
