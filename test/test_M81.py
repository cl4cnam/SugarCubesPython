from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	paral:
		generate 'e', None, 2
		branch:
			pause 2
			await 'e'
			await OR('e', 'f')
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
