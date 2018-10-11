from SugarCubes import *

test = Actor(
	Parex('e',
		Seq(
			Write('--> start'),
			Pause(),
			Repeat(10, Write("--> new"))
		)
	)
)

expected = '''
1 :
--> start
2 :
--> new
3 :
--> new
4 :
--> new
5 :
--> new
6 :
--> new
7 :
--> new
8 :
--> new
9 :
--> new
10 :
--> new
'''
