from SugarCubesLang import *

@sugarcube
def test():
	paral:
		killL 'e':
			pause forever
			print '--> e'
		branch:
			pause 4
			generate 'e'

expected = '''
1 :
2 :
3 :
4 :
5 :
6 :
--> e
7 :
8 :
9 :
10 :
'''
