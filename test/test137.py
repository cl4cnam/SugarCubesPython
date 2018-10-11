from SugarCubes import *

test = Actor(
	Par(
		Seq(
			ControlS('e',
				Write('--> e!')
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
--> e!
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
