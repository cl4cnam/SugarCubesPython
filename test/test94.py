from SugarCubes import *

test = Actor(
	Par(
		RepeatS(5,
			Generate('e'),
			Pause(),
			Generate('f')
		),
		RepeatS(3,
			Pause(1),
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
