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
			Generate('g'),
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
--> f
5 :
6 :
--> g
7 :
--> f
8 :
--> f
9 :
10 :
--> g
11 :
--> f
12 :
13 :
--> e
14 :
15 :
--> g
16 :
--> f
17 :
18 :
--> g
19 :
--> f
20 :
--> f
'''
