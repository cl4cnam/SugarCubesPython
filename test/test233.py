from SugarCubes import *

test = Par(
	RepeatForever(
		Kill('e',
			Seq(
				Await('e'),
				Pause(),
				Write('event &e is generated !')
			),
			Write('--> :p')
		)
	),
	RepeatForever(
		Pause(5),
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
7 :
--> :p
8 :
9 :
10 :
'''
