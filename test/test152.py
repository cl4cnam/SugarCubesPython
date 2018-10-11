from SugarCubes import *

test = Actor(
	Par(
		Seq(
			ControlS('e',
				RepeatS(2,
					Write('--> e!')
				)
			),
			Write('--> control end!')
		),
		RepeatS(5,
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
--> control end!
5 :
6 :
7 :
8 :
9 :
10 :
'''
