from SugarCubes import *

test = Actor(
	Par(
		RepeatS(3,
			Generate('e'),
			Generate('f')
		),
		RepeatS(1,
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
Hello World !
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
