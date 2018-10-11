from SugarCubes import *

test = Actor(
	Par(
		Seq(
			ControlS('e',
				RepeatS(2,
					Await('f'),
					Write('--> e!')
				)
			),
			Write('--> control end!')
		),
		RepeatS(5,
			Pause(1),
			Generate('e'),
		),
		RepeatS(2,
			Pause(1),
			Generate('f')
		)
	)
)

expected = '''
1 :
2 :
--> e!
3 :
4 :
--> e!
--> control end!
5 :
6 :
7 :
8 :
9 :
10 :
'''
