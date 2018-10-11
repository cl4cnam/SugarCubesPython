from SugarCubes import *

test = Actor(
	Par(
		Seq(
			Await('e'),
			Loop(Print("Hello World !"), 1)
		),
		Generate('e')
	)
)

expected = '''
1 :
Hello World !
2 :
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
