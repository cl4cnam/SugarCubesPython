from SugarCubes import *

test = Actor(
		Repeat(2,
			Repeat(2,
				Repeat(0,
					Print('Hello World !')
				)
			)
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
