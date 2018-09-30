from SugarCubes import *

test = Actor(
	Par(
		Repeat(
			Generate('e'),
			2
		),
		Seq(
			Pause(2),
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
