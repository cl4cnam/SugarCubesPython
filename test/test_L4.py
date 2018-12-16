from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	pause(3)
	print('Hello World !')

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
