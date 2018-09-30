from SugarCubes import *

test = Actor(
	Seq(
		Pause(),
		Diffuse('e'),
		Await('e'),
		Print('Hello World !')
	)
)

expected = '''
1 :
2 :
Hello World !
3 :
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
