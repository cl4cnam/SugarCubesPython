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
			Pause(),
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
4 :
--> f!
5 :
--> g!
6 :
7 :
8 :
--> f!
9 :
10 :
'''
