from SugarCubes import *

test = Actor(
		Seq(
			Pause(3),
			Print('Hello World !')
		)
)

expected = '''
1 :
2 :
3 :
4 :
Hello World !
5 :
6 :
7 :
8 :
9 :
10 :
'''
