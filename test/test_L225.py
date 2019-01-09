from SugarCubesLang import *

globalCond = True

def go():
	global globalCond
	globalCond = False

def fun():
	return globalCond

@sugarcube
def test():
	paral:
		ifRepeat fun:
			print '--> hello'
		seq:
			pause 5
			action go

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
