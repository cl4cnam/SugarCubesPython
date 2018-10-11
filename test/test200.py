from SugarCubes import *

maxI = 20

test = Actor(
	Par(
		Repeat(forever,
			When('e',
				When(And('f', 'g'),
					Write('--> f'),
					Write('--> g')
				),
				Write('--> e')
			)
		),
		Repeat(forever,
			Generate('e', None, 5),
			Pause(1)
		),
		Repeat(forever,
			Pause(1),
			Generate('f'),
			Pause(1),
			Generate('f'),
			Generate('g')
		)
	)
)

expected = '''
1 :
2 :
--> g
3 :
--> f
4 :
5 :
--> g
6 :
7 :
--> e
8 :
9 :
--> g
10 :
11 :
--> g
12 :
13 :
--> e
14 :
15 :
--> g
16 :
17 :
--> g
18 :
19 :
--> e
20 :
'''
