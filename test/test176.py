from SugarCubes import *

def async(m):
	m.generateEvent('$sens1')

test = Actor(
	Repeat(forever,
		Write('--> start'),
		Pause(1),
		# ProgControl('$sens1',
		ControlS('$sens1',
			Kill('g',
				Seq(
					Pause(1),
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
--> start
2 :
3 :
--> gen
--> await
--> to
4 :
5 :
6 :
7 :
--> go
--> after
8 :
--> start
9 :
10 :
--> gen
--> await
--> to
'''
