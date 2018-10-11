from SugarCubes import *

test = Actor(
	Par(
		Kill('e', PauseForever(), Write('--> e')),
		Seq(Pause(4), Generate('e'))
	)
)

expected = '''
1 :
2 :
3 :
4 :
5 :
6 :
--> e
7 :
8 :
9 :
10 :
'''
