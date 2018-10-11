from SugarCubes import *

test = Actor(
	Repeat(forever,
		Pause(1),
		# ProgControl('$sens1',
		ControlS('$sens1',
			Kill('g',
				Seq(
					Pause(2),
					Par(
						Seq(
							Write('--> gen'),
							Generate('f'),
							Write('--> await'),
							Await('e'),
							Write('--> after')
						),
						Seq(
							Write('--> to'),
							Pause(4),
							Write('--> go'),
							Generate('e')
						),
					)
				)
			)
		)
	)
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
