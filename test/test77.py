from SugarCubes import *

test = Actor(
	Par(
		Diffuse('f'),
		Seq(
			Diffuse('f'),
			Await('e'),
			Await(And('e', 'f')),
			Print('Hello World !')
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
