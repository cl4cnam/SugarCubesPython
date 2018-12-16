from SugarCubesLang import *

@sugarcube
def test():
	paral:
		control 'e':
			print '--> e!'
		branch:
			pause
			generate 'e'

expected = '''
1 :
2 :
--> e!
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
