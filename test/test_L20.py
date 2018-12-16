from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	repeat 2:
		repeat 3:
			repeat 1:
				print('Hello World !')

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
Hello World !
7 :
8 :
9 :
10 :
'''
