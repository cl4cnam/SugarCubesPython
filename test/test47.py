from SugarCubes import *

test = Actor(
	Seq(
		Pause(2),
		Diffuse('e'),
		Await('e'),
		Print('Hello World !')
	)
)

expected = '''
1 :
2 :
3 :
Hello World !
4 :
5 :
6 :
7 :
8 :
9 :
10 :
'''
