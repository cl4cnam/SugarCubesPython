from SugarCubes import *

test = Actor(
	Par(
		Repeat(4, When('e', Write('--> f'), Write('--> e'))),
		Repeat(4, Pause(0), Generate('e'))
	)
)

expected = '''
1 :
--> f
2 :
--> f
3 :
--> f
4 :
--> f
5 :
6 :
7 :
8 :
9 :
10 :
'''
