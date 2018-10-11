from SugarCubes import *

class Conf:
	def compute(self):
		print('--> compute')

maxI = 30
conf = Conf()
conf.val = 0

test = Par(
	Kill('e',
		Seq(
			Write('--> init'),
			Generate('f'),
			Par(
				ControlS(And('zone1', 'zone2'),
					Repeat(forever,
						Match([conf, 'val'],
							Write('==> case 0'),
							Write('==> case 1'),
							Write('==> case 2'),
							Write('==> case 3'),
							Write('==> case 4'),
						),
						Pause(10),
						Write('--> done'),
						Pause(),
						Action(conf.compute)
					)
				),
				Generate('inGame', 2, forever)
			)
		)
	),
	Seq(
		Pause(),
		Repeat(13,
			Generate('zone1'),
			Generate('zone2')
		)
	)
)

expected = '''
1 :
--> init
2 :
==> case 0
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
11 :
12 :
--> done
13 :
--> compute
14 :
==> case 0
15 :
16 :
17 :
18 :
19 :
20 :
21 :
22 :
23 :
24 :
25 :
26 :
27 :
28 :
29 :
30 :
'''
