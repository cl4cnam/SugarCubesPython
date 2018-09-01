from SugarCubes import *

test = {
	'program':
		Repeat(
			Repeat(
				Repeat(
					Print('Hello World !'),
					2
				),
				1
			),
			2
		)
	,
	'expected': '''
1 :
Hello World !
2 :
Hello World !
3 :
Hello World !
4 :
Hello World !
5 :
6 :
7 :
8 :
9 :
10 :
'''
}
