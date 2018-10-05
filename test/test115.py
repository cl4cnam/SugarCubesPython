from SugarCubes import *

test = Actor(
	Par(
		RepeatS(forever,
			KillS('f',
				RepeatS(forever,
					Await('e'),
					Write('Hello World !')
				),
				Write('--> f!')
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
--> f!
4 :
--> g!
5 :
Hello World !
6 :
7 :
--> f!
8 :
9 :
10 :
'''
