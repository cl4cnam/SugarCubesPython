from SugarCubes import *

test = Actor(
	Par(
		RepeatS(5,
			Generate('e'),
			Pause(0),
			Generate('f'),
			Pause(0)
		),
		RepeatS(3,
			Pause(4),
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
Hello World !
6 :
7 :
8 :
9 :
10 :
'''
