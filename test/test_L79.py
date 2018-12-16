from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	paral:
		branch:
			generate 'f', None, 2
		branch:
			pause
			await 'e'
			await AND('e', 'f')
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
