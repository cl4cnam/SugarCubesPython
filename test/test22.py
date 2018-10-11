from SugarCubes import *

test = Actor(
		Repeat(2,
			Repeat(1,
				Repeat(2,
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
6 :
7 :
8 :
9 :
10 :
'''
