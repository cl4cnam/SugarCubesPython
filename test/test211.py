from SugarCubes import *

test = Actor(
	Parex('e',
		Seq(
			Write('--> start'),
			Pause(),
			Repeat(10, Write('--> bip'))
		),
		Seq(
			Pause(),
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
--> new
4 :
--> bip
--> new
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
9 :
--> bip
10 :
--> bip
'''
