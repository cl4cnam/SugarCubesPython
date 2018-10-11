from SugarCubes import *

test = Actor(
	Par(
		Seq(
			ControlS('e',
				RepeatS(5,
					Write('--> e!')
				)
			),
			Write('--> control end!')
		),
		RepeatS(2,
			Pause(2),
			Generate('e'),
		),
	)
)

expected = '''
1 :
2 :
3 :
--> e!
4 :
5 :
6 :
--> e!
7 :
8 :
9 :
10 :
'''
