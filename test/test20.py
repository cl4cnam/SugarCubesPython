from SugarCubes import *

test = Actor(
		Repeat(2,
			Repeat(3,
				Repeat(1,
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
8 :
9 :
10 :
'''
