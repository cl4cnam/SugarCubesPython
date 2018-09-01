from SugarCubes import *

test = {
	'program':
		Repeat(
			Repeat(
				Repeat(
					Print('Hello World !'),
					3
				),
				2
			),
			1
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
Hello World !
6 :
Hello World !
7 :
8 :
9 :
10 :
'''
}
