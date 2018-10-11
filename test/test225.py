from SugarCubes import *

globalCond = True

def go():
	global globalCond
	globalCond = False

def fun():
	return globalCond

test = Actor(
	IfRepeat(fun, Write('--> hello')),
	Seq(Pause(5), Action(go))
)

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
9 :
10 :
'''
