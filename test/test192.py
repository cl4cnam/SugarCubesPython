from SugarCubes import *

test = Actor(
	Par(
		Repeat(2, When('e', Write('--> f'), Write('--> e'))),
		Repeat(2, Pause(0), Generate('e'))
	)
)

expected = '''
1 :
--> f
2 :
--> f
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
