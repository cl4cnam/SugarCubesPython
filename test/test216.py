from SugarCubes import *

test = Actor(
	Par(
		Parex('e',
			Seq(
				Write('--> start'),
				Pause(),
				Repeat(10, Generate('f'))
			),
			Repeat(10, Await('f'), Write('--> bip'))
		),
		Seq(
			Pause(3),
			Generate('e', Repeat(5, Write('--> new')))
		)
	)
)

expected = '''
1 :
--> start
2 :
--> bip
3 :
--> bip
4 :
--> bip
5 :
--> bip
--> new
6 :
--> bip
--> new
7 :
--> bip
--> new
8 :
--> bip
--> new
9 :
--> bip
--> new
10 :
--> bip
'''
