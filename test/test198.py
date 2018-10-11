from SugarCubes import *

test = Actor(
	Par(
		Repeat(5,
			When('e',
				When(And('f', 'g'),
					Write('--> f'),
					Write('--> g')
				),
				Write('--> e')
			)
		),
		Repeat(forever,
			Generate('e', None, 5)
		),
		Repeat(5,
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
--> f
7 :
8 :
--> g
9 :
10 :
'''
