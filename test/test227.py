from SugarCubes import *

def fun():
	print('--> hello')

test = Action(fun, forever)

expected = '''
1 :
--> hello
2 :
--> hello
3 :
--> hello
4 :
--> hello
5 :
--> hello
6 :
--> hello
7 :
--> hello
8 :
--> hello
9 :
--> hello
10 :
--> hello
'''
