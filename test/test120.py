from SugarCubes import *

test = Actor(
	Par(
		RepeatS(forever,
			Kill('f',
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
			Pause(0),
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
--> f!
3 :
--> g!
4 :
Hello World !
5 :
6 :
7 :
8 :
9 :
10 :
'''
