from SugarCubes import *

test = Actor(
	Seq(
		Diffuse('e'),
		Diffuse('f'),
		Await('e'),
		Await(Or('e', 'f')),
		Print('Hello World !')
	)
)

expected = '''
1 :
Hello World !
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
