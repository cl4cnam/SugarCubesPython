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
		Pause(),
		Generate('e')
	),
)

expected = '''
1 :
2 :
3 :
--> :p
--> e ?
4 :
5 :
--> :p
--> e ?
6 :
7 :
--> :p
--> e ?
8 :
9 :
--> :p
--> e ?
10 :
'''
