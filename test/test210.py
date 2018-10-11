from SugarCubes import *

test = Actor(
	Parex('e',
		Seq(
			Write('--> start'),
			Pause(),
			Repeat(10, Write('--> bip'))
		),
		Seq(
			Generate('e', Repeat(5, Write('--> new')))
		)
	)
)

expected = '''
1 :
--> start
2 :
--> bip
--> new
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
8 :
--> bip
9 :
--> bip
10 :
--> bip
'''
