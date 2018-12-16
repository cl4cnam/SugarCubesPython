from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	paral:
		repeat 5:
			generate 'e'
			pause 0
			generate 'f'
			pause 0
		repeat 3:
			pause 3
			await 'e'
			await AND('e', 'f')
			print 'Hello World !'

expected = '''
1 :
2 :
3 :
4 :
Hello World !
5 :
6 :
7 :
8 :
9 :
10 :
'''
