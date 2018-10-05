from SugarCubes import *

test = Actor(
	Par(
		Seq(
			Generate('e'),
			Pause(0),
			Generate('f'),
		),
		Seq(
			Await('f'),
			Await(And('e', 'f')),
			Write('Hello World !')
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
