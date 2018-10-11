from SugarCubes import *

test = Par(
	RepeatForever(
		Kill('e',
			Seq(
				Await('e'),
				Pause(),
				Write('e !')
			),
			Seq(
				Write('--> :p'),
				Write('--> e ?')
			)
		)
	),
	RepeatForever(
		Pause(4),
		Generate('e')
	),
)

expected = '''
1 :
2 :
3 :
4 :
5 :
6 :
--> :p
--> e ?
7 :
8 :
9 :
10 :
'''
