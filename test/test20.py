from SugarCubes import *

test = Actor(
		Repeat(
			Repeat(
				Repeat(
					Print('Hello World !'),
					1
				),
				3
			),
			2
		)
)

expected = '''
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
