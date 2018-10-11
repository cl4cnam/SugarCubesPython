from SugarCubes import *

def async(m):
	global sctest_count
	sctest_count += 1
	if sctest_count%2 == 0:
		m.generateEvent('$sens1')

def onSensor(v):
	print('==> $sens1')

maxI = 20
sctest_count = 0

test = Actor(
	Par(
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
		),
		ActionOn('$sens1', onSensor, None, forever)
	)
)

expected = '''
1 :
--> start
2 :
==> $sens1
3 :
4 :
==> $sens1
--> gen
--> await
--> to
5 :
6 :
==> $sens1
7 :
8 :
==> $sens1
--> go
--> after
9 :
--> start
10 :
==> $sens1
11 :
12 :
==> $sens1
--> gen
--> await
--> to
13 :
14 :
==> $sens1
15 :
16 :
==> $sens1
--> go
--> after
17 :
--> start
18 :
==> $sens1
19 :
20 :
==> $sens1
--> gen
--> await
--> to
'''
