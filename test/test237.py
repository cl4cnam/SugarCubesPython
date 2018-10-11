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
		Pause(2),
		Generate('e')
	),
)

expected = '''
1 :
2 :
3 :
4 :
--> :p
--> e ?
5 :
6 :
7 :
--> :p
--> e ?
8 :
9 :
10 :
--> :p
--> e ?
'''
