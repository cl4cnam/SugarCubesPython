from SugarCubes import *

test = Actor(
	Repeat(forever,
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
						Pause(6),
						Write('--> go'),
						Generate('e')
					),
				)
			)
		)
	)
)

expected = '''
1 :
2 :
3 :
--> gen
--> await
--> to
4 :
5 :
6 :
7 :
8 :
9 :
--> go
--> after
10 :
'''
