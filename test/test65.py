from SugarCubes import *

test = Actor(
	Seq(
		Pause(4),
		Diffuse('f'),
		Await('e'),
		Diffuse('f'),
		Await('f'),
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
