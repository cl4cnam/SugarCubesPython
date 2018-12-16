from SugarCubesLang import *

@sugarcube
def test():
	paral:
		repeat 5:
			when 'e':
				when AND('f', 'g'):
					print('--> f')
					print('--> g')
				print '--> e'
		repeat forever:
			generate 'e', None, 5
		repeat 5:
			pause 1
			generate 'f'
			pause 1
			generate 'f'
			generate 'g'

expected = '''
1 :
2 :
--> g
3 :
--> f
4 :
5 :
--> g
6 :
--> f
7 :
8 :
--> g
9 :
10 :
'''
