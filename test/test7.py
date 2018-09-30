from SugarCubes import *

test = Actor(
		Repeat(
			Print('Hello World !'),
			1
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
