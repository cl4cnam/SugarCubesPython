from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	paral:
		repeat 3:
			generate 'e'
			generate 'f'
		branch:
			pause 2
			await 'e'
			await AND('e', 'f')
			print 'Hello World !'

expected = '''
1 :
2 :
3 :
Hello World !
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
