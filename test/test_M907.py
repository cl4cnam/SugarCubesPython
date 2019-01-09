from SugarCubesLang import *

@sugarcube
def test():
	a = 100
	b = 7
	pause
	e = ( a <= b )
	pause
	print('--> ' + str(e))

expected = '''
1 :
2 :
3 :
--> False
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
