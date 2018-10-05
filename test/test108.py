from SugarCubes import *

test = Actor(
	Par(
		RepeatS(3,
			Pause(0),
			Await('e'),
			Await(And('e', 'f')),
			Write('Hello World !')
		),
		RepeatS(5,
			Generate('e'),
			Generate('f'),
			Pause(2)
		)
	)
)

expected = '''
1 :
Hello World !
2 :
3 :
4 :
Hello World !
5 :
6 :
7 :
Hello World !
8 :
9 :
10 :
'''
