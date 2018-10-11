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
		Pause(3),
		Generate('e')
	),
)

expected = '''
1 :
2 :
3 :
4 :
5 :
--> :p
--> e ?
6 :
7 :
8 :
9 :
--> :p
--> e ?
10 :
'''
