from SugarCubes import *

test = Actor(
	Par(
		RepeatS(forever,
			Kill('f',
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
--> f!
5 :
--> g!
6 :
7 :
--> f!
8 :
9 :
10 :
--> f!
'''
