from SugarCubesLang import *

@sugarcube(10, printInstant=True)
def test():
	pause(2)
	print('Hello World !')

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
