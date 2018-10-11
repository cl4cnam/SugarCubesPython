from SugarCubes import *

test = Actor(
	Par(
		ControlS('e',
			Write('--> e!')
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
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
