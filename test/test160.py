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
			Pause(2),
			Generate('f')
		)
	)
)

expected = '''
1 :
2 :
3 :
4 :
5 :
6 :
--> e!
7 :
8 :
9 :
10 :
'''
