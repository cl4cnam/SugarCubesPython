from SugarCubesLang import *

def async(m):
	m.generateEvent('$sens1')

maxI = 12

@sugarcube
def test():
	repeat forever:
		print '--> start'
		pause 1
		control '$sens1':
			execWithStopOnS 'g':
				pause 1
				paral:
					branch:
						print '--> gen'
						generate 'f'
						print '--> await'
						await 'e'
						print '--> after'
					branch:
						print '--> to'
						pause 2
						print '--> go'
						generate 'e'

expected = '''
1 :
--> start
2 :
3 :
--> gen
--> await
--> to
4 :
5 :
--> go
--> after
6 :
--> start
7 :
8 :
--> gen
--> await
--> to
9 :
10 :
--> go
--> after
11 :
--> start
12 :
'''
