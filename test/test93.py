from SugarCubes import *

test = Actor(
	Par(
		RepeatS(5,
			Generate('e'),
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
Hello World !
3 :
4 :
Hello World !
5 :
6 :
7 :
8 :
9 :
10 :
'''
