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
				Write('--> e ?'),
				Pause()
			)
		)
	),
	RepeatForever(
		Pause(0),
		Generate('e')
	),
)

expected = '''
1 :
2 :
--> :p
--> e ?
3 :
4 :
5 :
--> :p
--> e ?
6 :
7 :
8 :
--> :p
--> e ?
9 :
10 :
'''
