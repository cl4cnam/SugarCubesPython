from SugarCubes import *

test = Actor(
		Repeat(1,
			Repeat(3,
				Repeat(3,
					Print('Hello World !')
				)
			)
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
Hello World !
8 :
Hello World !
9 :
Hello World !
10 :
'''
