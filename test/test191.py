from SugarCubes import *

test = Actor(
	Par(
		Repeat(2, When('e', Write('--> f'), Write('--> e'))),
		Seq(Pause(0), Generate('e'))
	)
)

expected = '''
1 :
--> f
2 :
3 :
--> e
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
