from SugarCubes import *

test = Actor(
	Par(
		GenerateM('e', None, 3),
		Seq(
			Pause(2),
			Await('e'),
			Await(Or('e', 'f')),
			Write('Hello World !')
		)
	)
)

expected = '''
1 :
2 :
3 :
Hello World !
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
