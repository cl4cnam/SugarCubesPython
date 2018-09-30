from SugarCubes import *

test = Actor(
	Par(
		GenerateM('e', None, 2),
		Seq(
			Pause(),
			Await('e'),
			Await(Or('e', 'f')),
			Write('Hello World !')
		)
	)
)

expected = '''
1 :
2 :
Hello World !
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
