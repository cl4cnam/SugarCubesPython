from SugarCubesLang import *

def aggregMin(pList_val):
	return [min(pList_val)]

@sugarcube
def test():
	a = 3
	pause
	ifRepeat a < 40:
		a = a + 10
		print('--> ' + str(a))

expected = '''
1 :
2 :
--> 3
3 :
--> 13
4 :
--> 23
5 :
--> 33
6 :
--> 43
7 :
8 :
9 :
10 :
'''
