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
		RepeatS(4,
			Pause(1),
			Generate('e'),
		),
	)
)

expected = '''
1 :
2 :
--> e!
3 :
4 :
--> e!
5 :
6 :
--> e!
7 :
8 :
--> e!
9 :
10 :
'''
