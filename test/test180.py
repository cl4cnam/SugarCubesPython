from SugarCubes import *

def asyncPre(m):
	m.generateEvent('$sens1')

maxI = 20

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
							Pause(2),
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
--> go
--> after
6 :
--> start
7 :
8 :
--> gen
--> await
--> to
9 :
10 :
--> go
--> after
11 :
--> start
12 :
13 :
--> gen
--> await
--> to
14 :
15 :
--> go
--> after
16 :
--> start
17 :
18 :
--> gen
--> await
--> to
19 :
20 :
--> go
--> after
'''
