from SugarCubes import *

test = Par(
	Kill('e',
		Par(
			Seq(
				Kill('f',
					Seq(
						Await('e'),
						Pause(),
						Write('--> e !')
					),
					Seq(
						Write('--> :p'),
						Write('--> e ?'),
						Pause()
					),
				),
				Generate('e')
			)
		)
	),
	RepeatForever(
		Pause(10),
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
8 :
9 :
10 :
'''
