from SugarCubes import *

test = Actor(
	Seq(
		Pause(2),
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
