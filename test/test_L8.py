from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	repeat 2:
		print('Hello World !')

expected = '''
1 :
Hello World !
2 :
Hello World !
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''