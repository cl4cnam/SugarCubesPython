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
			Pause(3),
			Generate('e'),
		),
	)
)

expected = '''
1 :
2 :
3 :
4 :
--> e!
5 :
6 :
7 :
8 :
--> e!
9 :
10 :
'''
