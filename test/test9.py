from SugarCubes import *

test = Actor(
		Repeat(
			Print('Hello World !'),
			3
		)
)

expected = '''
1 :
Hello World !
2 :
Hello World !
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
