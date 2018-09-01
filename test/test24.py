from SugarCubes import *

test = {
	'program':
		Repeat(
			Repeat(
				Repeat(
					Print('Hello World !'),
					0
				),
				2
			),
			2
		)
	,
	'expected': '''
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
}
