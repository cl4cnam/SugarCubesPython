from SugarCubes import *

test = Actor(
	Par(
		When('e', Write('--> f'), Write('--> e')),
		Seq(Pause(2), Generate('e'))
	)
)

expected = '''
1 :
2 :
--> e
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
