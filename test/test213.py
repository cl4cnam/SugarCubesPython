from SugarCubes import *

test = Actor(
	Parex('e',
		Seq(
			Write('--> start'),
			Pause(),
			Repeat(10, Write('--> bip'))
		),
		Seq(
			Pause(2),
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
--> new
9 :
--> bip
10 :
--> bip
'''
