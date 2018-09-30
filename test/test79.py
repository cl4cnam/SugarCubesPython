from SugarCubes import *

test = Actor(
	Par(
		GenerateM('f', None, 2),
		Seq(
			Pause(),
			Await('e'),
			Await(And('e', 'f')),
			Write('Hello World !')
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
