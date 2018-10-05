from SugarCubes import *

test = Actor(
	Par(
		RepeatS(forever,
			Kill('f',
				RepeatS(forever,
					Await('e'),
					Write('Hello World !')
				)
			),
			Pause(),
			Generate('g')
		),
		RepeatS(5,
			Generate('e')
		),
		RepeatS(3,
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
--> g!
5 :
Hello World !
6 :
7 :
8 :
9 :
10 :
'''
