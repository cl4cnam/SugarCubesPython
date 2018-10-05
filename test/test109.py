from SugarCubes import *

test = Actor(
	Par(
		Kill('f',
			RepeatS(5,
				Await(And('e', 'f')),
				Write('Hello World !')
			)
		),
		RepeatS(5,
			Generate('e'),
			Generate('f'),
		)
	)
)

expected = '''
1 :
Hello World !
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
