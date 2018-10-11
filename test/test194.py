from SugarCubes import *

test = Actor(
	Par(
		Repeat(4, When('e', Write('--> f'), Write('--> e'))),
		Repeat(4, Pause(1), Generate('e'))
	)
)

expected = '''
1 :
2 :
--> e
3 :
4 :
--> e
5 :
6 :
--> e
7 :
8 :
--> e
9 :
10 :
'''
