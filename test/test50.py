from SugarCubes import *

test = Actor(
	Seq(
		Diffuse('e'),
		Pause(4),
		Await('e'),
		Print('Hello World !')
	)
)

expected = '''
1 :
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