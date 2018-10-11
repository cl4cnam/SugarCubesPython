from SugarCubes import *

test = Actor(
	Par(
		Seq(
			ControlS('e',
				RepeatS(0,
					Write('--> e!')
				)
			),
			Write('--> control end!')
		),
		Seq(
			Pause(),
			Generate('e'),
		),
	)
)

expected = '''
1 :
2 :
--> control end!
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
