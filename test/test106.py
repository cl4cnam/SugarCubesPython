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
			Pause(0),
			Await('e'),
			Await(And('e', 'f')),
			Write('Hello World !')
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
5 :
6 :
7 :
8 :
9 :
10 :
'''
