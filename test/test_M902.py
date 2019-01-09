from SugarCubesLang import *

@sugarcube
def test():
	a = '--> Hello'
	a = '--> Hi'
	pause
	print('|' + a + ' !')

expected = '''
1 :
2 :
|--> Hello !
|--> Hi !
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
