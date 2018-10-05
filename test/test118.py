from SugarCubes import *

test = Actor(
	Par(
		RepeatS(forever,
			KillS('f',
				RepeatS(forever,
					Await('e'),
					Write('Hello World !')
				),
				Seq(
					Await('f'),
					Write('--> f!')
				)
			),
			Pause(),
			Generate('g')
		),
		RepeatS(5,
			Generate('e')
		),
		RepeatS(4,
			Pause(2),
			Generate('f')
		),
		Seq(
			Await('g'),
			Write('--> g!')
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
--> f!
7 :
--> g!
8 :
9 :
10 :
'''
