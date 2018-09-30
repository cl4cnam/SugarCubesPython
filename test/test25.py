from SugarCubes import *

test = Actor(
		Repeat(
			Repeat(
				Repeat(
					Print('Hello World !'),
					2
				),
				0
			),
			2
		)
)

expected = '''
1 :
2 :
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
