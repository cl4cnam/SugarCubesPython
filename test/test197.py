from SugarCubes import *

test = Actor(
	Par(
		Repeat(5, When('e', Write('--> f'), Write('--> e'))),
		Repeat(5, Pause(1), Generate('e'), Pause(1), Generate('e'))
	)
)

expected = '''
1 :
2 :
--> e
3 :
--> f
4 :
5 :
--> e
6 :
--> f
7 :
8 :
--> e
9 :
10 :
'''
